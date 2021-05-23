#include <windows.h>
#include <stdio.h>
#include <tchar.h>

#define BUF_SIZE 2048

int main(int argc, char** argv) {
    printf("HELLO!\n");
    int n_mappings = 3;
    HANDLE maph[n_mappings];
    const TCHAR* mappings[] = {
        TEXT("acpmf_physics"),
        TEXT("acpmf_graphics"),
        TEXT("acpmf_static"),
    };
    
    for (int i=0; i < n_mappings; i++) {
		const TCHAR *shmName = mappings[i];
		TCHAR szName[100];
		_stprintf(szName, TEXT("Local\\%s"), shmName);
		
    	maph[i] = CreateFileMapping(INVALID_HANDLE_VALUE, NULL, PAGE_READWRITE, 0, BUF_SIZE, szName);
    	if (maph[i] == NULL)
    	{
        	printf("Could not create file mapping object (%ld).\n", GetLastError());
        	return 1;
   		}
	}
	
    Sleep(10000);
	for (int i=0; i < n_mappings; i++) {
			if (maph[i] != NULL) CloseHandle( maph[i] );
	}
	
    return 0;
}
