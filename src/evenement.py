class FakeMouseEvent:
    def __init__(self, touch):
        self.client_x = touch.clientX
        self.client_y = touch.clientY

# Souris appuyée
def on_mouse_down(ev, terrain, fenetre, menu):
    # Données de la souris
    rect = fenetre.main_canvas.getBoundingClientRect()
    mx = (ev.clientX - rect.left)
    my = (ev.clientY - rect.top)
    icon_clique = menu.detection_icon_clique(mx, my)
    if not icon_clique:
        terrain.detection_tuile_clique(mx, my)
    
# Souris bouge
def on_mouse_move(ev, terrain, fenetre):
    rect = fenetre.main_canvas.getBoundingClientRect()
    mx = (ev.clientX - rect.left)
    my = (ev.clientY - rect.top)

# # Doigt touche
# def on_touch_start(ev, terrain, fenetre):
#     # Empêcher le scroll
#     ev.preventDefault()
#     # Premier doit
#     touch = ev.touches[0]
#     # faux évènement
#     fake_event = FakeMouseEvent(touch)
#     on_mouse_down(fake_event, terrain, fenetre)

# # Doigt lâche
# def on_touch_end(ev, terrain, fenetre):
#     ev.preventDefault()
#     touch = ev.changedTouches[0]
#     # faux évènement
#     fake_event = FakeMouseEvent(touch)
#     on_mouse_up(fake_event, terrain, fenetre)

# # Doigt bouge
# def on_touch_move(ev, terrain, fenetre):
#     ev.preventDefault()
#     if ev.touches:
#         touch = ev.touches[0]
#         # faux évènement
#         fake_event = FakeMouseEvent(touch)
#         on_mouse_move(fake_event, terrain, fenetre)

def creer_evenement(terrain, fenetre, menu):
    # Evenements souris
    fenetre.main_canvas.bind("mousedown", lambda ev: on_mouse_down(ev, terrain, fenetre, menu))
    # fenetre.main_canvas.bind("mouseup", lambda ev: on_mouse_up(ev, terrain, fenetre))
    # fenetre.main_canvas.bind("mousemove", lambda ev: on_mouse_move(ev, terrain, fenetre))

    # # Evenements tactile
    # fenetre.main_canvas.bind("touchstart", lambda ev: on_touch_start(ev, terrain, fenetre))
    # fenetre.main_canvas.bind("touchend", lambda ev: on_touch_end(ev, terrain, fenetre))
    # fenetre.main_canvas.bind("touchmove", lambda ev: on_touch_move(ev, terrain, fenetre))