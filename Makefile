MINGW_PFX = i686-w64-mingw32
# MINGW_PFX = x86_64-w64-mingw32

.DUMMY: all

all: acc_wrapper.exe _acc.exe

acc_wrapper.exe: acc_wrapper.c
	$(MINGW_PFX)-gcc $< -o $@ -O0 -msse2 # -shared-libgcc
	# $(MINGW_PFX)-strip --strip-unneeded $@

_acc.exe: acc_exe.c
	$(MINGW_PFX)-gcc $< -o $@ -O0 -msse2 # -shared-libgcc
	# $(MINGW_PFX)-strip --strip-unneeded $@

clean:
	@rm -v acc_wrapper.exe _acc.exe