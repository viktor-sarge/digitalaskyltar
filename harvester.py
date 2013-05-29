#    Copyright 2013 Regionbibliotek Halland
#
#    This file is part of Digitala skyltar.
#
#    Digitala skyltar is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Digitala skyltar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Digitala skyltar.  If not, see <http://www.gnu.org/licenses/>.
from vbgopacbookharvester import VarbergOpacHarvester

typeCachedRssHarvester = 'CachedRSSHarvester'
typeWordpressHarvester = 'WordpressHarvester'

def getHarvester(dsd, settings, addandcheckfunc):
    """Return the appropriate harvester for a given type
    
    Arguments
    dsd -- the datasource description containing the desired harvester type
    settings -- parameter that is passed to the harvester
    addandcheckfunc -- parameter that is passed to the harvester
    
    """
    if(dsd.type == typeCachedRssHarvester):
        return VarbergOpacHarvester(dsd, settings, addandcheckfunc)
    else:
        raise Exception('Unknown harvester type ' + dsd.type)
