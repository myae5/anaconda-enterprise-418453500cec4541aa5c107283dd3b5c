import intake

p = intake.open_catalog('catalog.yml').gui
p.plot_widget.value = True
p.servable('Intake GUI')
