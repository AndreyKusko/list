from django.shortcuts import redirect, render


def apple_touch_icon(request):
    return redirect('/static/logo_v4.2_tab_icon_v0.0_apple_touch_icon_v0.1.png')
