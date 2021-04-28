$image = "Space_Images_1/" 
$date = Get-Date -Format "yyyy-MM-dd"
$image + "" + $date
print $image
set-itemproperty -path "HKCU:Control Panel\Desktop" -name wallpaper -value $image