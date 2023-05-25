xrandr --setprovideroutputsource modestting NVIDIA-0
xrandr --auto
xrdb -merge ~/.Xresources
xrandr --output DP1 --below eDP1

exec i3 
[-f ~/.xprofile] && . ~/.xprofile
