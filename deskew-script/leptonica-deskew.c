#include <stdio.h>
#include <string.h>
#include "allheaders.h" 

int main(int argc, char *argv[]) {
	char filename[20];
	strcpy(filename, "deskewed/"); //!!!ATT: you need to have a dir called deskewed in the current dir
    strcat(filename,argv[1]); //concatenates the name of the file with the name of the dir

    PIX* pix = pixRead(filename);
    pixDeskew(pix,0);
	pixWrite(filename,pix, IFF_TIFF);
	pixDestroy(&pix);

	return 0;
}