all: rele

rele: RCSwitch.o rele.o
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $+ -o $@ -lwiringPi
	cp $@ ../
clean:
	$(RM) *.o rele
