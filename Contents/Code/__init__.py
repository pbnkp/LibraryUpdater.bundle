####################################################################################################

PREFIX  = '/applications/libraryupdater'
NAME    = 'Library Updater'

ART     = 'art-default.jpg'
ICON    = 'icon-default.png'
PMS_URL = 'http://%s/library/sections/'

####################################################################################################

def Start():
    Plugin.AddPrefixHandler(PREFIX, MainMenu, NAME, ICON, ART)
    Plugin.AddViewGroup('List', viewMode='List', mediaType='items')

    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = 'List'
    DirectoryItem.thumb = R(ICON)
    PopupDirectoryItem.thumb = R(ICON)

####################################################################################################

def MainMenu():
    dir = MediaContainer(noCache=True)

    all_keys = []

    sections = XML.ElementFromURL(PMS_URL % (Prefs['host']), errors='ignore').xpath('//Directory')
    for section in sections:
        key = section.get('key')
        title = section.get('title')
        dir.Append(Function(PopupDirectoryItem(UpdateType, title='Update section "' + title + '"'), title=title, key=list(key)))
        all_keys.append(key)

    if len(all_keys) > 0:
      dir.Append(Function(PopupDirectoryItem(UpdateType, title='Update all sections'), title='All sections', key=all_keys))

    dir.Append(PrefsItem('Preferences', thumb=R('icon-prefs.png')))

    return dir

####################################################################################################

def UpdateType(sender, title, key):
    dir = MediaContainer()
    dir.Append(Function(DirectoryItem(UpdateSection, title='Normal update'), title=title, key=key, force=False))
    dir.Append(Function(DirectoryItem(UpdateSection, title='Force update'), title=title, key=key, force=True))
    return dir

####################################################################################################

def UpdateSection(sender, title, key, force):
    for section in key:
        url = PMS_URL % (Prefs['host'])  + section + '/refresh'
        if force:
            url += '?force=1'
        update = HTTP.Request(url, cacheTime=1).content

    if title == 'All sections':
        return MessageContainer(title, 'All sections will be updated!')
    elif len(key) > 1:
        return MessageContainer(title, 'All chosen sections will be updated!')
    else:
        return MessageContainer(title, 'Section "' + title + '" will be updated!')
