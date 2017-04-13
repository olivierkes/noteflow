UI := $(wildcard noteflow/ui/*.ui) $(wildcard noteflow/ui/*/*.ui) $(wildcard noteflow/ui/*/*/*.ui) $(wildcard noteflow/ui/*.qrc) 
UIs= $(UI:.ui=.py) $(UI:.qrc=_rc.py)
TS := $(wildcard i18n/*.ts)
QMs= $(TS:.ts=.qm)

ui: $(UIs)

run: $(UIs)
	bin/noteflow

man:
	/usr/lib/x86_64-linux-gnu/qt5/bin/assistant &

designer:
	/usr/lib/x86_64-linux-gnu/qt5/bin/designer &

debug: $(UIs)
	gdb --args python3 bin/noteflow

lineprof:
	kernprof -l -v bin/noteflow

profile:
	python3 -m cProfile -s 'cumtime' bin/noteflow | more

compile:
	cd noteflow && python3 setup.py build_ext --inplace
	
callgraph:
	cd noteflow; pycallgraph myoutput -- main.py

translation:
	pylupdate5 -noobsolete i18n/noteflow.pro
	
linguist:
	linguist i18n/noteflow_fr.ts
	lrelease i18n/noteflow_fr.ts
	
i18n: $(QMs)

pyinstaller:
	python3 /usr/local/bin/pyinstaller lotrdb.spec

%_rc.py : %.qrc
	pyrcc5 "$<" -o "$@" 

%.py : %.ui
# 	pyuic4  "$<" > "$@" 
	pyuic5  "$<" > "$@" 
	
%.qm:  %.ts
	lrelease "$<"

