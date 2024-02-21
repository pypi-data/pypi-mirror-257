# -*- coding: utf-8 -*-
# Copyright (C) 2017-2023 Team tiramisu (see AUTHORS for all contributors)
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# The original `Config` design model is unproudly borrowed from
# the rough pypy's guys: http://codespeak.net/svn/pypy/dist/pypy/config/
# the whole pypy projet is under MIT licence
# ____________________________________________________________
"""SynDynOptionDescription and SynDynLeadership internal option
it's an instanciate synoptiondescription
"""
from typing import Optional, Iterator, Any, List


from ..i18n import _
from ..setting import ConfigBag, undefined
from .baseoption import BaseOption
from .syndynoption import SynDynOption


class Syn:
    __slots__ = ('opt',
                 'rootpath',
                 '_suffixes',
                 )

    def __init__(self,
                 opt: BaseOption,
                 rootpath: str,
                 suffixes: list,
                 ) -> None:
        self.opt = opt
        self.rootpath = rootpath
        self._suffixes = suffixes

    def impl_get_display_name(self) -> str:
        return self.opt.impl_get_display_name(self)

    def get_child(self,
                  name: str,
                  config_bag: ConfigBag,
                  *,
                  allow_dynoption: bool=False,
                  ):
        """get children
        """
        # if not dyn
        option = self.opt.get_child_not_dynamic(name,
                                                allow_dynoption,
                                                )
        if option:
            if allow_dynoption and option.impl_is_dynoptiondescription():
                return option
            return option.to_dynoption(self.impl_getpath(),
                                       self._suffixes,
                                       )
        for child in self.opt._children[1]:  # pylint: disable=no-member
            if not child.impl_is_dynoptiondescription():
                continue
            for suffix in child.get_suffixes(config_bag,
                                             dynoption=self,
                                             ):
                if name != child.impl_getname(suffix):
                    continue
                return child.to_dynoption(self.impl_getpath(),
                                          self._suffixes + [suffix],
                                          )
        raise AttributeError(_(f'unknown option "{name}" '
                               f'in optiondescription "{self.impl_get_display_name()}"'
                               ))

    def get_children(self,
                     config_bag: ConfigBag,
                     ):
        # pylint: disable=unused-argument
        """get children
        """
        for child in self.opt._children[1]:
            if child.impl_is_dynoptiondescription():
                for suffix in child.get_suffixes(config_bag,
                                                 dynoption=self,
                                                 ):
                    yield child.to_dynoption(self.impl_getpath(),
                                             self._suffixes + [suffix],
                                             )
            else:
                yield child.to_dynoption(self.impl_getpath(),
                                         self._suffixes,
                                         )

    def get_children_recursively(self,
                                 bytype: Optional[BaseOption],
                                 byname: Optional[str],
                                 config_bag: ConfigBag,
                                 self_opt: BaseOption=None,
                                 ) -> BaseOption:
        # pylint: disable=unused-argument
        """get children recursively
        """
        for option in self.opt.get_children_recursively(bytype,
                                                        byname,
                                                        config_bag,
                                                        self,
                                                        ):
            yield option

    def get_suffixes(self) -> str:
        """get suffixes
        """
        return self._suffixes

    def impl_is_dynsymlinkoption(self) -> bool:
        """it's a dynsymlinkoption
        """
        return True


class SubDynOptionDescription(Syn):

    def impl_getpath(self) -> str:
        """get path
        """
        path = self.opt.impl_getname()
        if self.rootpath:
            path = f'{self.rootpath}.{path}'
        return path

    def getsubdyn(self):
        return self.opt.getsubdyn()

    def impl_is_optiondescription(self):
        return True

    def impl_is_symlinkoption(self):
        return False

    def impl_is_leadership(self):
        return False

    def impl_is_dynoptiondescription(self) -> bool:
        return True

    def impl_getproperties(self):
        return self.opt.impl_getproperties()


class SynDynOptionDescription(Syn):
    """SynDynOptionDescription internal option, it's an instanciate synoptiondescription
    """
    def __getattr__(self,
                    name: str,
                    ) -> Any:
        # if not in SynDynOptionDescription, get value in self.opt
        return getattr(self.opt,
                       name,
                       )

    def impl_getname(self) -> str:
        """get name
        """
        if self.opt.impl_is_dynoptiondescription():
            return self.opt.impl_getname(self._suffixes[-1])
        return self.opt.impl_getname()

    def impl_getpath(self) -> str:
        """get path
        """
        path = self.impl_getname()
        if self.rootpath:
            path = f'{self.rootpath}.{path}'
        return path

    def getsubdyn(self):
        return self.opt


class SynDynLeadership(SynDynOptionDescription):
    """SynDynLeadership internal option, it's an instanciate synoptiondescription
    """
    def get_leader(self) -> SynDynOption:
        """get the leader
        """
        return self.opt.get_leader().to_dynoption(self.impl_getpath(),
                                                  self._suffixes,
                                                  )

    def get_followers(self) -> Iterator[SynDynOption]:
        """get followers
        """
        subpath = self.impl_getpath()
        for follower in self.opt.get_followers():
            yield follower.to_dynoption(subpath,
                                        self._suffixes,
                                        )

    def pop(self,
            *args,
            **kwargs,
            ) -> None:
        """pop value for a follower
        """
        self.opt.pop(*args,
                     followers=self.get_followers(),
                     **kwargs,
                     )

    def follower_force_store_value(self,
                                   value,
                                   config_bag,
                                   owner,
                                   ) -> None:
        """force store value for a follower
        """
        self.opt.follower_force_store_value(value,
                                            config_bag,
                                            owner,
                                            dyn=self,
                                            )

    def get_suffixes(self) -> str:
        """get suffix
        """
        return self._suffixes
