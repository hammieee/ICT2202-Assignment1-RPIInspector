#!/bin/bash


echo "To: rainyraina23@gmail.com
Subject: Your password has expired
Content-Type: text/html; charset="us-ascii"
<html>
<h1>Your company password has expired. Please click this link to reset your password.</h1>
<p>https://forms.gle/9a1se59RpL1c94pM8</p>
</html>" > index.html


/usr/sbin/sendmail rainyraina23@gmail.com < index.html

