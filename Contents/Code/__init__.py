####################################################################################################

APPLICATIONS_PREFIX = "/applications/libraryupdater"

NAME = L('Library Updater')

ART         = 'art-default.png'
ICON        = 'icon-default.png'
PLEX_URL    = 'http://localhost:32400/library/sections'

####################################################################################################

def Start():

    Plugin.AddPrefixHandler(APPLICATIONS_PREFIX, MainMenu, L('Library Updater'), ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)

####################################################################################################

def MainMenu():

    dir = MediaContainer(viewGroup="InfoList")

    sectionsPage = HTML.ElementFromURL(PLEX_URL, errors='ignore')
    
    dir.Append(Function(DirectoryItem(UpdateSection, title='All Sections', subtitle='Force update of all sections'),
        section='all'))
    
    for section in sectionsPage.xpath('//directory'):
        key = section.get('key')
        title = section.get('title')
        dir.Append(Function(DirectoryItem(UpdateSection, title=title, subtitle='Force update of '+title+' section'),
            section=key))
    
    return dir

####################################################################################################

def UpdateSection(sender, section):
    '''Tell PMS to update the given section'''
    url = PLEX_URL +'/' + section + '/refresh?force=1'
    
    try:
        update = HTTP.Request(url, errors='ignore').content
    except:
        return MessageContainer(NAME, L('Force update failed.'))
        
    return MessageContainer(NAME, L('Force update started.'))
    