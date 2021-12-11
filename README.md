# Introduction
During a stream I was listening to, I was notified that there was an problem where current StreamDecks plugins do not have the features of fading in Spotify volumes.  
After looking more into it, it would seem like fading volumes was not the only features missing and the development space looks promising.  
Seeing this space and I've also been eager to try out Python and learning more about OAuth 2.0, I thought this was a good chance to play around.

# Goal
The goal of this API is to allow automations for Spotify.  
Below automations are split into 2 parts, the UI and backend part.

## UI
- Easy way to login and refresh tokens 
    - Usual streams are 3 hours, since access token expires in an hour, using refresh will give a better UX
- Easy way to access the features.
    - The current PoC requires you to input the actual URL paths, which is very inconvenient for streamers.  
    A button or proper frontend will make the UX better.
- Integrate with StreamDeck plugins
    - Most streamers use StreamDeck as their main stream event controller. A plugin integrated into StreamDeck will be a familiar experience for streamers

## Functionality
- Volume fading (fade in and fade out)

# PROBLEMS need solving before release
- Many user specific variables are handled as global variable (volume and device id for example). This ain't gonna work if more than one person uses this. Therefore use cookies or pass cur vol into the path itself.