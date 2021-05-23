#include <windows.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <tchar.h>


BOOL fileExists(TCHAR * file) {
   WIN32_FIND_DATA FindFileData;
   HANDLE handle = FindFirstFile(file, &FindFileData);
   BOOL found = handle != INVALID_HANDLE_VALUE;
   if (found) {
       FindClose(handle);
   }
   return found;
}

BOOL done = FALSE;
BOOL WINAPI CtrlHandler(DWORD fdwCtrlType)
{
    done = TRUE;
    return TRUE;
}

int main(int argc, char** argv) {
    WIN32_FIND_DATA fdata;
    LPDWORD ret;
    PROCESS_INFORMATION acc_pi;
    STARTUPINFO si = {sizeof(si)};
    TCHAR* EXE = TEXT("_acc.exe");
    TCHAR ARGS[255] = TEXT("_acc.exe");

    for(int i = 1; i < argc; i++) {
        _tcscat(ARGS, " ");
        _tcscat(ARGS, argv[i]);
    }

    int n_mappings = 3;        
    const TCHAR* mappings[] = {
        TEXT("acpmf_physics"),
        TEXT("acpmf_graphics"),
        TEXT("acpmf_static"),
    };
    HANDLE maph[n_mappings], fd[n_mappings];

    acc_pi.dwProcessId = 0;
    if (fileExists(EXE) && CreateProcess(EXE, ARGS, NULL,  NULL, FALSE,
            0, NULL, NULL, &si, &acc_pi) == 0 ) {
        printf("Unable to start %s\n", ARGS);
        return 1;
    }

    if (chdir("/dev/shm") != 0) {
        printf("Could not change directory to /dev/shm: %s\n", strerror(errno));
        goto wait;
    }

	for (int i=0; i < n_mappings; i++) {
		const TCHAR *shmName = mappings[i];
		TCHAR szName[100];
		_stprintf(szName, TEXT("Local\\%s"), shmName);

		fd[i] = CreateFile(shmName, GENERIC_READ|GENERIC_WRITE, FILE_SHARE_READ|FILE_SHARE_WRITE,
		                        NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
		if (fd[i] == INVALID_HANDLE_VALUE) {
		    printf("Could not open %s: %s\n", shmName, strerror(GetLastError()));
		    goto wait;
		}
		maph[i] = CreateFileMapping(fd[i], NULL, PAGE_READWRITE, 0, 2048, szName);
		if (maph[i] == NULL) {
		    printf("Could not create mapping for %s: %s\n", szName, strerror(GetLastError()));
		    CloseHandle(fd[i]);
		    goto wait;
		}
		printf("Bridged /dev/shm/%s to Win32 named mapping \"%s\"\n", shmName, szName);
    }

    if (acc_pi.dwProcessId > 0)
        printf("Done! Waiting for ACC to stop.\n");
    else
        printf("Done! Press CTRL-C to stop.\n");

wait:
    if (acc_pi.dwProcessId > 0) {
        WaitForSingleObject( acc_pi.hProcess, INFINITE );
        CloseHandle( acc_pi.hProcess );
        CloseHandle( acc_pi.hThread );
    } else {
        SetConsoleCtrlHandler(CtrlHandler, TRUE);
        while(!done) {
            Sleep(1000);
        }
    }

    for (int i=0; i < n_mappings; i++) {
		if (maph[i] != NULL) CloseHandle( maph[i] );
		CloseHandle( fd[i] );
		DeleteFile( mappings[i] );
	}
    return 0;
}
