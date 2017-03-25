UI := $(wildcard flownote/ui/*.ui) $(wildcard flownote/ui/*/*.ui) $(wildcard flownote/ui/*/*/*.ui) $(wildcard flownote/ui/*.qrc) 
UIs= $(UI:.ui=.py) $(UI:.qrc=_rc.py)
TS := $(wildcard i18n/*.ts)
QMs= $(TS:.ts=.qm)

ui: $(UIs)

run: $(UIs)
	bin/flownote

man:
	/usr/lib/x86_64-linux-gnu/qt5/bin/assistant &

designer:
	/usr/lib/x86_64-linux-gnu/qt5/bin/designer &

debug: $(UIs)
	gdb --args python3 bin/flownote

lineprof:
	kernprof -l -v bin/flownote

profile:
	python3 -m cProfile -s 'cumtime' bin/flownote | more

compile:
	cd flownote && python3 setup.py build_ext --inplace
	
callgraph:
	cd flownote; pycallgraph myoutput -- main.py

translation:
	pylupdate5 -noobsolete i18n/flownote.pro
	
linguist:
	linguist i18n/flownote_fr.ts
	lrelease i18n/flownote_fr.ts
	
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

