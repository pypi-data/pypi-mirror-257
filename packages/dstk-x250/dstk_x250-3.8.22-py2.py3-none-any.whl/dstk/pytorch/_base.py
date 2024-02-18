#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe de wrapping Scikit-Learn pour PyTorch

Created on Mon Oct 21 14:42:57 2019

@author: Cyrile Delestre
"""
import uuid
import pickle as pkl
import inspect
from types import FunctionType
from typing import (Optional, ByteString, Union, Callable, Dict, Any, List,
                    Tuple)
from functools import partial
from collections import OrderedDict
from warnings import warn
from pathlib import Path

import numpy as np
from sklearn.base import BaseEstimator
import torch
from torch.optim import Optimizer
from torch.nn.modules.loss import _Loss
from torch.nn.utils import clip_grad_norm_
from torch.nn.parallel.distributed import DistributedDataParallel as DDP
from torch.cuda.amp import GradScaler
from torch.utils.data import DataLoader, Dataset
from torch.utils.data.distributed import DistributedSampler

from dstk.pytorch._utils import check_tensor, is_dist_avail_and_initialized
from dstk.pytorch._callback import (CallbackInterface, CallbackHandler,
                                    FitState, FitControl)
from dstk.utils.errors import DivergenceError


def _getattr(model, attr):
    attr_split = attr.split('.')
    if len(attr_split) > 1:
        model = getattr(model, attr_split[0])
        return _getattr(model, '.'.join(attr_split[1:]))
    return getattr(model, attr_split[0])


def _setattr(model, attr, value):
    attr_split = attr.split('.')
    if len(attr_split) > 1:
        model = getattr(model, attr_split[0])
        return _setattr(model, '.'.join(attr_split[1:]), value)
    setattr(model, attr_split[0], value)


def get_params(model: BaseEstimator):
    r"""
    Fonction possédant le même comportement que la méthode get_params de
    Scikit-Learn mais ne revoit pas les attribues de classe DDP de Pytorch.
    """
    att_ddp = inspect.signature(DDP.__init__)
    att_mod = inspect.signature(model.__init__)
    parameters = [
        pp
        for pp in att_mod.parameters.values()
        if pp.name != "self"
            and pp.kind != pp.VAR_KEYWORD
            and pp not in att_ddp.parameters.values()
    ]
    for pp in parameters:
        if pp.king == pp.VAR_POSITIONAL:
            raise RuntimeError(
                "scikit-learn estimators shoud always "
                "specify their parameters in the signature "
                "of thier __init__ (no varargs)."
                "%s with constructor %s doesn't "
                "follow this convention." % (model, att_mod)
            )
    return sorted([pp.name for pp in parameters])


class BaseEnvironnement(BaseEstimator):
    r"""
    Classe d'environnement PyTorch pour être compatible Scikit-Learn.

    Notes
    -----
    Les attributs constituant BaseEnvironnement :
        _is_fitted: bool
            détermine si le modèle est entraîné

    Les méthodes constituant BaseEnvironnement :
        number_of_parameters:
            nombre de paramètre (entraînable ou non) constiuant la 
            modélisation
        save_model:
            sauvegarde du modèle via Pickle
        load_weights:
            chargement des poids via Pickle. Si modèle non buildé, build le 
            modèle
        load_model:
            chargement d'un modèle à partir du Pickle au format save_weights
        fit:
            fonction d'apprentissage avec prototypage compatible avec 
            Scikit-Learn

    Les méthodes qui doivent être implémentées dans la classe du réseau :
        __init__:
            avec seulement les hyper-paramètres du réseau, afin de pouvoir 
            modifier les hyper-paramètres avec la méthode set_params de 
            BaseEstimator.
        build:
            fonction d'implémentation des éléments du réseau PyTorch ainsi 
            que de l'attribut optimizer contenant l'optimizer du réseau
        forward:
            fonction PyTorch d'éxécution du réseau
        predict:
            fonction de prédiction, au prototypage Scikit-Learn 
            predict(X, **kargs) :
                - classifier : doit sortir une classe
                - regresseur : doit sortir une régression
        predict_proba: (optionnel)
            pour les classifier uniquement. Permet de sortir la probabilité 
            d'une observation dans chaqu'une des classes
        score: (optionnel)
            au format de prototype Scikit-Learn. Si cette méthode n'est pas 
            implémentée par l'utilisateur, ce sont alors les méthodes par 
            défaut dans Scikit-Learn qui seront utilisées, à savoir dans le 
            cas d'un Regressor, R^2, et dans le cas de Classifier, l'accuracy.
    """
    _is_fitted: bool = False

    def build(self):
        r"""
        Méthode d'erreur si la fonction build n'a pas été implémentée dans 
        la classe modèle de l'utilisateur.
        """
        raise NotImplementedError(
            "La méthode build n'a pas été implémentée dans la classe "
            f"{self.__name__}. Se reporter à la documentation de "
            "BaseEnvironnement pour connaître les commodités d'implémentation "
            "de cette dernière."
        )

    def forward(self):
        r"""
        Méthode de forward du module de réseau profond PyTorch (voir la
        documention PyTorch).
        """
        raise NotImplementedError(
            "La méthode forward n'a pas été implémentée dans la classe "
            f"{self.__name__}. Se reporter à la documentation de "
            "BaseEnvironnement et PyTorch pour connaître les commodités "
            "d'implémentation de cette dernière."
        )

    def number_of_parameters(self, learn_params: bool=True):
        r"""
        Méthope retournant le nombre de paramètres présent dans le modèle.

        Parameters
        ----------
        learn_params : bool (=True)
            Compte les paramètres qui permettent l'apprentissage du modèle. 
            Sinon compte tous les paramètres (ceux qui sont dérivables et 
            non dérivables).
        """
        if learn_params:
            model_parameters = filter(
                lambda p: p.requires_grad, self.parameters()
            )
        else:
            model_parameters = self.parameters()
        return sum([np.prod(p.shape) for p in model_parameters])

    def save_model(
        self,
        path: Optional[str] = None,
        *,
        save_optimizer_state: bool = False,
        attr_list: Optional[Union[List[str], Tuple[str]]] = None,
        **kargs_dump
    ):
        r"""
        Méthode permettant de sauvegarder simplement les paramètres et les
        poids du modèle (sans la structure de réseau). Utilise Pickle.

        Parameters
        ----------
        path: Optional[str]
            path directory du modèle, si None retourne les données binaires de 
            Pickle.dumps()
        save_state_optimizer: bool
            booléen de sauvegarde de l'état de l'optimizer (par défaut False).
        attr_list: Optional[Union[List[str], Tuple(str)]]
            liste d'attributs à sauvegarder (par défaut None).
        **kargs_dump:
            paramètres attachés à Pickle.dump(obj, file, **kargs_dump) si 
            path est un chemin ou a Pickles.dump(obj, **kargs_dump) si None.
        """
        # get_params est hérité de BaseEstimator
        mother_classes = self.__class__.__bases__
        if DDP not in mother_classes:
            params = self.get_params()
        else:
            params = get_params(self)
        state_dict = self.state_dict()
        if save_optimizer_state:
            state_optimizer = self.optimizer.state_dict()
        else:
            state_optimizer = None
        if attr_list:
            state_attribut = {
                attr: _getattr(self, attr) for attr in attr_list
            }
        else:
            state_attribut = None
        if isinstance(path, (str, Path)):
            pkl.dump(
                obj = [
                    params,
                    state_dict,
                    state_optimizer,
                    state_attribut
                ],
                file = open(path, 'bw'),
                **kargs_dump
            )
            return self
        elif path is None:
            return pkl.dumps(
                obj = [
                    params,
                    state_dict,
                    state_optimizer,
                    state_attribut
                ],
                **kargs_dump
            )
        else:
            raise AttributeError(
                "L'argument path doit être None ou un str et non de type "
                f"{type(path)}."
            )
        return self

    def load_weights(
        self, 
        path_or_bytes: Union[str, ByteString],
        **kargs_load
    ):
        r"""
        Méthode permettant de charger les poids et les paramètres du modèle
        via Pickle.

        Parameters
        ----------
        path_or_bytes: Union[str, ByteString]
            path directory du modèle ou bytes représentant le modèles
        **kargs_load:
            paramètres attachés à Pickle.load(file, **kargs_load) si path ou 
            Pickle.loads(data, **kargs_load) si bytes.
        """
        if not hasattr(self, 'build'):
            raise NotImplementedError(
                "Le modèle PyTorch n'a pas de méthode build (réf. doc de "
                "la classe)."
            )
        self.build()
        if isinstance(path_or_bytes, (str, Path)):
            _, state_dict, state_optimizer, state_attribut = pkl.load(
                file = open(path_or_bytes, 'br'),
                **kargs_load
            )
        elif isinstance(path_or_bytes, bytes):
            _, state_dict, state_optimizer, state_attribut = pkl.loads(
                data = open(path_or_bytes, 'br'),
                **kargs_load
            )
        else:
            raise AttributeError(
                "path_or_bytes doit être soit de type str ou bytes et non "
                f"de type {type(path_or_bytes)}."
            )
        self.load_state_dict(state_dict);
        if state_optimizer:
            self.optimizer.load_state_dict(state_optimizer)
        if state_attribut:
            for key, item in state_attribut.items():
                _setattr(self, key, item);
        self.eval()
        return self

    @classmethod
    def load_model(
        cls,
        path_or_bytes: Union[str, ByteString],
        **kargs_load
    ):
        r"""
        Fonction permettant de charger un modèle à partir d'une sauvegarde au
        format Pickle issue de save_weights(path).

        Parameters
        ----------
        path_or_bytes: Union[str, ByteString]
            path directory du modèle ou bytes représentant le modèles
        **kargs_load:
            paramètres attachés à Pickle.load(file, **kargs_load) si path ou 
            Pickle.loads(data, **kargs_load) si bytes.

        Returns
        -------
        model: BaseEnvironnement
            modèle chargé
        """
        if isinstance(path_or_bytes, (str, Path)):
            params, state_dict, state_optimizer, state_attribut = pkl.load(
                file = open(path_or_bytes, 'br'),
                **kargs_load
            )
        elif isinstance(path_or_bytes, bytes):
            params, state_dict, state_optimizer, state_attribut = pkl.loads(
                data = path_or_bytes,
                **kargs_load
            )
        else:
            raise AttributeError(
                "path_or_bytes doit être soit de type str ou bytes et non "
                f"de type {type(path_or_bytes)}."
            )
        model = cls(**params)
        if not hasattr(model, 'build'):
            raise NotImplementedError(
                "Le modèle PyTorch n'a pas de méthode build (réf. doc de la "
                "classe)."
            )
        model.build();
        model.load_state_dict(state_dict);
        if state_optimizer:
            model.optimizer.load_state_dict(state_optimizer)
        if state_attribut:
            for key, item in state_attribut.items():
                _setattr(model, key, item)
        model.eval()
        return model

    def _extract_state(self, model):
        r"""
        Méthode privée qui extrait les paramètres du modèle et clone les 
        tensors PyTorch.

        Parameters
        ----------
        model:
            un modèle
        """
        return OrderedDict(
            (kk, vv.detach().clone()) for kk, vv in model.state_dict().items()
        )

    def _divergence(self, loss: float):
        r"""
        Méthode interne d'alerte de divergence du modèle pendant sa phase 
        d'apprentissage.
        """
        loss_ = loss.cpu()
        if np.isnan(loss_) or np.isinf(loss_):
            raise DivergenceError(
                """Verger ! L'algorithme a dit "verger" !"""
            )

    def _mod(self, n, mod):
        r"""
        Méthode interne permettant de calculer le modulo.
        """
        if mod:
            return n % mod
        else:
            return None

    def _train_step(
        self,
        data: List[Dict[str, Any]],
        loss_fn: Callable,
        loss_kargs: Dict[str, Any],
        state : FitState,
        control: FitControl,
        list_callbacks: Optional[List[CallbackInterface]] = None
    ):
        r"""
        Méthode privée d'une étape de backpropagation du gradient.

        Parameters
        ----------
        data: List[Dict[str, Any]]
            Liste de dictionnaires sur les données d'un mini-batch.
        loss_fn: Callable
            Fonction coût PyTorch.
        loss_kargs: Dict[str, Any]
            Dictionnaire d'arguments à utiliser dans la fonction de coût 
            loss_fun.
        state: FitState
            Etat de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        control: FitControl
            Contrôle de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        list_callbacks: Optional[List[CallbackInterface]]
            Liste des callback permettant de contôler l'apprentissage durant 
            la phase d'évaluation.

        Returns
        -------
        loss: Valeur de la fonction coût au travers du mini-batch.
        """
        if list_callbacks:
            list_callbacks.begin_step(self, data, state, control, None)
        state.n_iter += 1
        iter_accu = state.n_iter % control.gradient_accumulation == 0
        self.train()
        if control.device.type != "cpu":
            for key, value in data.items():
                if key not in control.expected_key_to_device:
                    if isinstance(data[key], (list, tuple,)):
                        data[key] = [ii.to(control.device) for ii in data[key]]
                    else:
                        data[key] = value.to(control.device)
        with torch.autocast(
            device_type=control.device.type,
            enabled=control.mixed_type_gpu
        ):
            output = self.forward(**data)
            if control.target_checktensor:
                target = check_tensor(data[control.target_field])
            else: target = data[control.target_field]
            loss_ = loss_fn(output, target, **loss_kargs)
        if control.gradient_accumulation > 1:
            loss_ /= control.gradient_accumulation
            if (
                control.is_distributed
                and hasattr(self, 'no_sync')
                and not iter_accu
            ):
                with self.no_sync:
                    control.grad_scaler.scale(loss_).backward()
            elif (
                control.is_distributed
                and not hasattr(self, 'no_sync')
                and not iter_accu
            ):
                warn(
                    "Instance distribué, mais le modèle ne possède pas de "
                    "contexte no_sync ce qui est un comportement anormale."
                )
                control.grad_scaler.scale(loss_).backward()
            else:
                control.grad_scaler.scale(loss_).backward()
        else:
            control.grad_scaler.scale(loss_).backward()
        if iter_accu:
            if control.max_gradient_norm:
                control.grad_scaler.unscale_(self.optimizer)
                clip_grad_norm_(self.parameters(), control.max_gradient_norm)
            control.grad_scaler.step(self.optimizer)
            control.grad_scaler.update()
            self.optimizer.zero_grad()
        loss = loss_.detach()
        self._divergence(loss)
        if list_callbacks:
            list_callbacks.end_step(self, data, state, control, loss)
        return loss

    def _eval_step(
        self,
        data: List[Dict[str, Any]],
        loss_fn: Callable,
        loss_kargs: Dict[str, Any],
        control : FitControl
    ):
        r"""
        Méthode privée d'une étape deévaluation.

        Parameters
        ----------
        data: List[Dict[str, Any]]
            Liste de dictionnaires sur les données d'un mini-batch.
        loss_fn: Callable
            Fonction coût PyTorch.
        loss_kargs: Dict[str, Any]
            Dictionnaire d'arguments à utiliser dans la fonction de coût 
            loss_fun.
        control: FitControl
            Contrôle de l'apprentissage (instancé dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).

        Returns
        -------
        loss: Valeur de la fonction coût au travers du mini-batch.
        """
        if control.device.type != "cpu":
            for key, value in data.items():
                if key not in control.expected_key_to_device:
                    if isinstance(data[key], (list, tuple,)):
                        data[key] = [ii.to(control.device) for ii in data[key]]
                    else:
                        data[key] = value.to(control.device)
        with torch.no_grad():
            self.eval()
            output = self.forward(**data)
            if control.target_checktensor:
                target = check_tensor(data[control.target_field])
            else: target = data[control.target_field]
            loss = loss_fn(output, target, **loss_kargs)
        loss = loss.detach()
        self._divergence(loss)
        return loss

    def _iter_eval(
        self,
        eval_dataset: DataLoader,
        loss_fn: Callable,
        loss_kargs: Optional[Dict[str, Any]],
        state: FitState,
        control: FitControl,
        list_callbacks: Optional[List[CallbackInterface]] = None
    ):
        r"""
        Méthode interne exécutant la phase d'évaluation durant l'apprentissage.
        Cette étape peut être appelé à la fin d'une époque ou durant 
        l'éxécution de l'époque (dépend de l'arguement iter_eval de la méthode 
        :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).

        Parameters
        ----------
        eval_dataset: DataLoader
            Dataset d'évaluation au format DataLoeader généré dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`.
        loss_fn: Callable
            Fonction coût à minimiser (utiliser les fonctions présentes dans 
            torch.nn.functional). Si la fonction est une fonction custom, elle 
            doit avoir le prototypage suivant :
                - loss_fn(y_estim, y_true, reduction='sum', **kargs)
            avec une implémentation de réduction 'sum' pour les phases 
            d'évaluation et 'mean' pour les phases d'apprentissage.
        loss_kargs: Optional[Dict[str, Any]]
            Dictionnaire d'arguments à utiliser dans la fonction de coût 
            loss_fun.
        state: FitState
            Etat de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        control: FitControl
            Contrôle de l'apprentissage (instancé dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        list_callbacks: Optional[List[CallbackInterface]]
            Liste des callback permettant de contôler l'apprentissage durant 
            la phase d'évaluation.
        """
        if list_callbacks:
            list_callbacks.begin_eval(
                model=self,
                data=eval_dataset,
                state=state,
                control=control,
                res_loss=None
            )
        loss_eval = 0
        for jj, eval_batch in enumerate(eval_dataset):
            list_callbacks.begin_eval_step(
                model=self,
                data=eval_batch,
                state=state,
                control=control,
                res_loss=loss_eval/(jj+1)
            )
            try:
                loss_eval += self._eval_step(
                    data=eval_batch,
                    loss_fn=loss_fn,
                    loss_kargs=loss_kargs,
                    control=control
                )
            except DivergenceError as error:
                control.diverge = True
                warn(error.msg)
                break
        if list_callbacks:
            list_callbacks.end_eval(
                model=self,
                data=eval_dataset,
                state=state,
                control=control,
                res_loss=loss_eval/(jj+1)
            )

    def fit(
        self,
        X: Union[List[Dict[str, Any]], Dataset, DataLoader],
        y: Optional[List[Union[int, float]]] = None,
        *,
        eval_dataset: Optional[DataLoader] = None,
        target_field: str = 'target',
        target_checktensor: bool = True,
        loss_fn: _Loss,
        loss_kargs: Dict[str, Any] = dict(),
        optimizer: Optional[Optimizer] = None,
        optimizer_kargs: Dict[str, any] = dict(),
        nb_epoch: int,
        iter_eval: Optional[int] = None,
        callbacks: Optional[List[CallbackInterface]] = None,
        device: str = 'cuda:0',
        mixed_type_gpu: bool = False,
        expected_key_to_device: List[str] = list(),
        gradient_accumulation: Optional[int] = None,
        max_gradient_norm: Optional[float] = None,
        dataloader_kargs: Dict[str, Any] = dict(),
        begin_apply_fn: Callable = lambda self: None,
        end_apply_fn: Callable = lambda self: None,
        n_jobs: Optional[int] = None,
        state: Optional[FitState] = None,
        control: Optional[FitControl] = None,
        build: bool = True
    ):
        r"""
        Méthode de fitting généralisé du module PyTorch.

        Parameters
        ----------
        X: Union[List[Dict[str, Any]], Dataset, DataLoader]
            Dataset PyTorch contenant dans un dictionnaire les infos 
            nécessaires pour l'apprentissage du modèle.
        y: Optional[List[Union[int, float]]] 
            Pour être ISO avec Scikit-learn. L'ensemble de l'apprentissage
            passera via X et le système DataSet et DataLoader de PyTorch.
        eval_dataset: Optional[DataLoader]
            DataLoader PyTorch contenant les observations et les targets 
            d'évaluation. Si eval_dataset est None alors pas de early stopping 
            et évaluation des performances sur les données d'entrainement 
            (déconseillé car très fort risque d'overfitting).
        target_field: str (='target')
            Nom du champ contenu dans X de la target. Par défaut "target". 
            Attention l'implémentation de la foction collate_fn, peut faire 
            changer le nom de la target.
        target_checktensor: bool (=True)
            Permet de checker si le champs target est un tensor, sinon le
            converti. Si False ne checke pas si le champs est un tensor.
        loss_fn: _Loss
            Fonction coût à minimiser (utiliser les fonctions présentes dans 
            torch.nn.functional). Si la fonction est une fonction custom, elle 
            doit avoir le prototypage suivant :
                - loss_fn(y_estim, y_true, reduction='sum', **kargs)
            avec une implémentation de réduction 'sum' pour les phases 
            d'évaluation et 'mean' pour les phases d'apprentissage.
        loss_kargs: Dict[str, Any]
            Dictionnaire d'arguments à utiliser dans la fonction decoût 
            loss_fun. Si il n'y a pas d'arguments, mettre un dictionnaire 
            vide.
        optimizer: Optional[Optimizer]
            Objet optimizer de PyTorch. Si non renseigné doit être implémenté 
            dans le modèle et dans la partie build. Utile si un paramètre de 
            l'optimizer doit faire partie des hyperparamètres. Sinon à 
            renseigner ici pour alléger l'implémentation globale. Cela peut
            être un optimizer instancier à l'exétieur, pour celà test si
            'param_groups' est un attribu qui existe. Si c'est le cas
            'optimizer_kargs' ne sera pas pris en compte.
        optimizer_kargs: Dict[str, any]
            Paramètres pour l'optimizer, si optimizer inclue dans la 
            modélisation et l'argument optimizer est à None cet argument ne 
            sera pas pris en compte.
        nb_epoch: int (=5)
            Nombre d'époques max de l'apprentissage.
        iter_eval: Optional[int]
            Nombre d'itération entre deux évaluations. Actif seulement si 
            eval_set est non None. Si iter_eval est à None (définit par 
            défaut) les évaluations du modèle seront à la fin des époques. 
            Si un entier positif est renseigné les évaluations auront lieu 
            tous les iter_eval itérations d'apprentissage.
        callbacks: Optional[List[CallbackInterface]]
            Liste de callback intervenant aux différentes étapes de 
            l'entraînement et de l'évaluation. Pour avoir la liste des 
            différents callbacks implémentés par défaut voir 
            :func:`~dstk.pytorch._callback`.
        device: str (='cuda:0')
            Indique le device sur le quel l'apprentissage s'exécute.
        mixed_type_gpu: bool (=False)
            Utilisation de nVidia AMP (Automatic Mixed Precision) pour GPU 
            permettant le typage mixte FP16 et FP32.
        expected_key_to_device: List[str] (=list())
            Liste des variables à exclure vers la charge sur GPU.
        gradient_accumulation: Optional[int]
            Nombre d'itération d'entrainement avec back propagation du 
            gradient avant d'appliquer la descente de gradient.
        max_gradient_norm: Optional[float]
            Valeur maximum du gradient, sinon clipping de ce dernier par la 
            valeur max_gradient_norm. Si non renseigné alors pas de gradient 
            clipping. Le clipping du gradient peut être utilie pour l'approche 
            par accumulation des gradient.
        dataloader_kargs: Dict[str, Any] (=dict())
            Si X n'est pas un objet Dataloader permet d'entrer les arguments 
            du Dataloader (voir la `documention PyTorch_ `pour connaitre les 
            arguments du Dataloader).
        begin_apply_fn: Callable (=lambda: None)
            Fonction appelé avant l'entrainement. Peut faire référence à
            self à l'intérieur et permettre de changer un comportement du
            modèle au moment de l'appel de la méthode fit par un autre module
            (RandomizedSearchCV de Scikit-Learn par exemple).
        end_apply_fn: Callable (=lambda: None)
            Fonction appelé à la fin de l'entrainement. Peut faire référence à
            self à l'intérieur et permettre de changer un comportement du
            modèle au moment de l'appel de la méthode fit par un autre module
            (RandomizedSearchCV de Scikit-Learn par exemple).
        n_jobs: Optional[int]
            Nombre de process des étapes d'inférence et de backpropagation des 
            gradients :
                - Si y est not None :
                    forcé à 1 ;
                - Si None :
                    utilise automatiquement le nombre de processeurs 
                    (et pas le nombre de threads) ;
                - Si un entier :
                    utilise le nombre de processus indiqué.
        state: Optional[FitState]
            Etat de l'apprentissage (instancié dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        control: Optional[FitControl]
            Contrôle de l'apprentissage (instancé dans la méthode 
            :func:`~dstk.pytorch._base.BaseEnvironnement.fit`).
        build: bool (=True)
            Permet de reconstruire le réseau si, entre la définition de la 
            classe et le fit, il y a changement d'hyper-paramètres (exemple : 
            RandomizedSearchCV ou toute autre fonction Scikit-learn pouvant 
            utiliser set_params).

        Warnings
        --------
        Si le but du modèle est d'être utilisé avec d'autre module 
        Scikit-Learn il ne faut pas que le type de X soit un DataLoader 
        (les autres types reste valide). De manière général, pour la méthode 
        fit, il est conseillé d'utiliser le type DataSet PyTorch comme type 
        d'entré à X.

        **Attention pour les TPU** :

        Les passage de référence dans la construction du graph du type :

        >>> DummiesModel(Module, BaseEnvironnement)
        >>>     def __ini__(self):
        >>>         super().__init__()
        >>>         [...]
        >>>
        >>>     def build(self):
        >>>         self.dense1 = Linear(10, 5)
        >>>         self.dense2 = Linear(10, 5)
        >>>         # liaison des poids
        >>>         self.dense1.weight = self.dense2.weigth
        [...]
        
        ne fonctionne pas sur les devices TPU car les poids sont copiés
        systématiquement. Il faudra relier de nouveau les poids une fois
        sur le TPU.

        >>> DummiesModel(Module, BaseEnvironnement)
        >>>     def __ini__(self):
        >>>         super().__init__()
        >>>         [...]
        >>>
        >>>     def build(self):
        >>>         self.dense1 = Linear(10, 5)
        >>>         self.dense2 = Linear(10, 5)
        >>>         # liaison des poids
        >>>         self.dense1.weight = self.dense2.weigth
        >>>
        >>>     def post_move_to_tpu(self):
        >>>         self.dense1.weight = self.dense2.weigth
        [...]

        .. _documention PyTorch: https://pytorch.org/docs/stable/data.html
        """
        if not hasattr(self, 'optimizer') and optimizer is None:
            raise NotImplementedError(
                "L'estimateur ne possède par d'objet 'optimizer'. Cette "
                "attribue doit être un objet d'otimisation de type PyTorch : "
                "torch.optim.(SGD, ADAM, etc.). Il faut le déclarer dans "
                "la construction de la classe modèle ou le définir dans "
                "les arguments de la méthode fit."
            )

        if iter_eval is not None and iter_eval < 0:
            raise AttributeError(
                "iter_eval doit être soit None ou un entier positif."
            )

        if (
            gradient_accumulation is not None
            and iter_eval < gradient_accumulation
        ):
            warn(
                "iter_eval < gradient_accumulation donc à chaque itération "
                "un pas de gradient ne sera pas effectué."
            )

        if (
            is_dist_avail_and_initialized()
            and not isinstance(X, DataLoader)
            and not isinstance(X.sampler, DistributedSampler)
        ):
            raise AttributeError(
                "Vous être dans une instance parallélisé et le séquenceur "
                "du dataset d'entraînement n'est pas de type "
                "DistributedSampler !"
            )
        elif (
            not is_dist_avail_and_initialized()
            and isinstance(X, DataLoader)
            and isinstance(X.sampler, DistributedSampler)
        ):
            warn(
                "La dataset d'entraînement possède un séquenceur prévu pour "
                "du multi-node/muti-GPU. Il ce peut que ce soit un "
                "comportement non souhaité."
            )

        # Permet de construire le modèle avec les paramètres actuels du fit.
        if build:
            self.build()

        if optimizer is not None:
            if hasattr(self, 'optimizer'):
                warn(
                    "Un optimizer a été donné en argument de la méthode fit "
                    "hors il en existait déjà un attribue optimizer dans la "
                    "classe du modèle. La priorité est accordé à celui en "
                    "entré du fit et à donc écrasé celui du modèle de base."
                )
            if hasattr(optimizer, 'param_groups'):
                self.optimizer = optimizer
            else:
                self.optimizer = optimizer(
                    self.parameters(),
                    **optimizer_kargs
                )

        list_callbacks = CallbackHandler(callbacks)
        list_callbacks.copy()

        id_processes = str(uuid.uuid1())

        if not isinstance(X, DataLoader):
            if isinstance(X, dict):
                X = [X]
            dataset = DataLoader(
                dataset=X,
                **dataloader_kargs
            )
        else:
            dataset = X

        # Si y est non None c'est que le processes passe par un search de
        # Scikit-Learn.
        if y is not None and n_jobs is None:
            torch.set_num_threads(1)
            dataset.num_workers = 0
        elif n_jobs is not None:
            torch.set_num_threads(n_jobs)
        else:
            torch.set_num_threads(torch.get_num_threads())

        if not state:
            if isinstance(loss_fn, FunctionType):
                loss_name = loss_fn.__name__
            elif isinstance(loss_fn, partial):
                loss_name = loss_fn.func.__name__
            else:
                loss_name = loss_fn.__class__.__name__
            state = FitState(
                id_process=id_processes,
                nb_epoch=nb_epoch,
                epoch_max_steps=len(dataset),
                eval_max_steps=len(eval_dataset) if eval_dataset else 0,
                loss_name=loss_name,
                n_iter=0
            )
        if not control:
            control = FitControl(
                target_field=target_field,
                target_checktensor=target_checktensor,
                device=(
                    device := torch.device(
                        device if torch.cuda.is_available() else 'cpu'
                    )
                ),
                mixed_type_gpu=mixed_type_gpu and device.type != "cpu",
                grad_scaler=GradScaler(
                    enabled=(mixed_type_gpu and device.type != "cpu")
                ),
                expected_key_to_device=expected_key_to_device,
                gradient_accumulation=gradient_accumulation,
                max_gradient_norm=max_gradient_norm
            )
        self.to(control.device)
        if control.device.type != "tpu" and hasattr(self, 'post_move_to_tpu'):
            self.post_move_to_tpu()
        if isinstance(loss_fn, FunctionType):
            co_varnames = loss_fn.__code__.co_varnames
        elif isinstance(loss_fn, partial):
            co_varnames = loss_fn.func.__code__.co_varnames
        else:
            co_varnames = loss_fn.__class__.forward.__code__.co_varnames
        state_in_loss = list(
            filter(
                lambda x: 
                    (
                        x.lower() == 'state'
                        or x.lower() == 'fitstate'
                        or x.lower() == 'fit_state'
                    ),
                co_varnames
            )
        )
        state_in_loss_kargs = list(
            filter(lambda x: x == 'kargs' or x == 'kwargs', co_varnames)
        )
        if len(state_in_loss) == 1:
            loss_kargs[state_in_loss[0]] = state
        elif len(state_in_loss) > 1:
            warn(
                "Plusieurs clefs trouvé pouvant correspondre à l'argument "
                "state dans les entrées de la fonction loss : "
                f"{', '.join(state_in_loss)}, du coupe ne nom d'argument "
                "state sera choisi par défaut."
            )
            loss_kargs['state'] = state
        elif len(state_in_loss_kargs) == 1:
            loss_kargs['state'] = state

        begin_apply_fn(self)
        list_callbacks.begin_train(self, dataset, state, control, None)
        try:
            for n_epoch in range(nb_epoch):
                if control.is_distributed:
                    if hasattr(dataset.sampler, 'set_epoch'):
                        dataset.sampler.set_epoch(n_epoch)
                    if (
                        eval_dataset
                        and hasattr(
                            eval_dataset.sampler, 
                            'set_epoch'
                        )
                    ):
                        eval_dataset.sampler.set_epoch(n_epoch)
                    torch.distributed.barrier()
                state.n_epoch = n_epoch
                loss_epoch = 0
                list_callbacks.begin_epoch(
                    model=self,
                    data=dataset,
                    state=state,
                    control=control,
                    res_loss=loss_epoch
                )
                for ii, batch in enumerate(dataset):
                    if (
                        eval_dataset
                        and self._mod(state.n_iter, iter_eval) == 0
                    ):
                        if control.is_master:
                            self._iter_eval(
                                eval_dataset=eval_dataset,
                                loss_fn=loss_fn,
                                loss_kargs=loss_kargs,
                                state=state,
                                control=control,
                                list_callbacks=list_callbacks
                            )
                            if control.diverge or control.training_stop:
                                break
                        if control.is_distributed:
                            torch.distributed.barrier()
                    try:
                        loss_step = self._train_step(
                            data=batch,
                            loss_fn=loss_fn,
                            loss_kargs=loss_kargs,
                            state=state,
                            control=control,
                            list_callbacks=list_callbacks
                        )
                        loss_epoch += loss_step
                    except DivergenceError as error:
                        control.diverge = True
                        warn(error.msg)
                        break
                loss_epoch /= (ii+1)
                list_callbacks.end_epoch(
                    model=self,
                    data=dataset,
                    state=state,
                    control=control,
                    res_loss=loss_epoch
                )
        except (Exception, KeyboardInterrupt) as e:
            list_callbacks.error_interrupt(
                model=self,
                data=dataset,
                state=state,
                control=control,
                res_loss=None,
                exception=e
            )
            if isinstance(e, KeyboardInterrupt):
                warn(
                    "\n"
                    "------------------------------------------\n"
                    "| Fin du training par KeyboardInterrupt. |\n"
                    "------------------------------------------\n"
                    "\n"
                )
            else:
                raise e
        list_callbacks.end_train(self, dataset, state, control, None)
        if control.device.type != "cpu": self.to(torch.device('cpu:0'))
        self._is_fitted = True
        end_apply_fn(self)
        return self
