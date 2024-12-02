//=======================================================================
// Copyright (c) 2019 Gitterer
// Distributed under the terms of the MIT License.
// (See accompanying file LICENSE or copy at
//  http://opensource.org/licenses/MIT)
//=======================================================================


#pragma warning (disable : 4996)
// #include "stdafx.h"
#include <iostream>
#include <fstream>
#include <cstring>
#include <string>
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <vector>
#include <set>
#include <iterator>
#include <algorithm>
#include <memory>

#include <filesystem>
using namespace std;

ifstream images;
ifstream labels;
const int w =32, h = 32;
const int row_size = 9999;
int labelr[row_size];
int *red[w + 1];
int *green[w + 1];
int *blue[w + 1];
const int nDatasize = 10000;
int x = 1;
int y = 1;
int offset = 1;

void init_array() {
	for (int i = 1; i <= w; ++i) {
		red[i] = new int[w + 1];
		green[i] = new int[w + 1];
		blue[i] = new int[w + 1];
	}
}
void getpixel(int pixel_val,  string s_val) {

	char s_val_char = s_val[0];
	
	if (offset < 0x21)
	{
		if (int(pixel_val) >0) {
			switch (s_val_char) {
			case 'r':    
				red[x][y - 1] = pixel_val;
				break;
			case 'g':  
				green[x][y - 1] =  pixel_val;
				break;
			case 'b':         
				blue[x][y - 1] = pixel_val;
				break;
			}
			

		}
		else {
			// add 0x100 because of the range of signed char
			// signed char -0x80 to 0x7F 
			//this is because the value of signed char compensates for data loss by counting into negative to give values out of range
			//0x80 + 0x7F is 0xFF .
			switch (s_val_char) {
			case 'r':
				red[x][y - 1] = 0x100 + pixel_val;
				break;
			case 'g':
				green[x][y - 1] = 0x100 + pixel_val;
				break;
			case 'b':
				blue[x][y - 1] = 0x100 + pixel_val;
				break;
			}
			
		}

		++y;
		++offset;
	}
	if (offset > 0x20) {
		if (y > 0x20)
			++x;
			if (x> 0x20) x = 1;

		y = 1;
		offset = 1;
	}

}
void reader(int startval, int endval, string dataset) {
	
	string training_image_fn;
	char datasetval = dataset[0];
	switch (datasetval) {
		case '1':
			 training_image_fn = "cifar-10-batches-bin/data_batch_1.bin";
		break;
		case '2':
			 training_image_fn = "cifar-10-batches-bin/data_batch_2.bin";
		break;
		case '3':
			 training_image_fn = "cifar-10-batches-bin/data_batch_3.bin";
			break;
		case '4':
			 training_image_fn = "cifar-10-batches-bin/data_batch_4.bin";
			break;
		case '5':
			training_image_fn = "cifar-10-batches-bin/data_batch_4.bin";
			break;
		case 't': 
			 training_image_fn = "cifar-10-batches-bin/test_batch.bin";
			break;
	}

	images.open(training_image_fn, std::ios::in | std::ios::binary | std::ios::ate);
	if (!images) {
		std::cout << "Error opening file: " << training_image_fn << std::endl;
		return;
	}
	
	
	register auto file_size = images.tellg();

	std::unique_ptr<char[]> BYTEREAD(new  char[file_size]);

	//Read the entire file at once
	images.seekg(0, std::ios::beg);
	images.read(BYTEREAD.get(), file_size);

	images.close();
	int size = 10000;
	if (endval == 0)size = 10000;


	for (int i = startval; i < size; ++i) {
		labelr[i] = BYTEREAD[i * 3073];
		for (int j = 1; j < 3073; ++j) {

			 if (j < 1025 ) getpixel((int)(BYTEREAD[i * 3073 + j]), "r");
			 
			 if (j> 1024 && j < 2049) getpixel((int)(BYTEREAD[i * 3073 + j]), "g");
			 
			 if (j > 2048) getpixel((int)(BYTEREAD[i * 3073 + j]), "b");
			 
		}
		break;
	}

}
void rw_file(string z) {

	int w = 32, h = 32;
	int x, y;
	int r, g, b;
	FILE *f;
	unsigned char *img = NULL;
	int filesize = 54 + 3 * w*h;  //w is your image width, h is image height, both int

	img = (unsigned char *)malloc(3 * w*h);
	memset(img, 0, 3 * w*h);


	for (int i = 0; i<w; i++)
	{
		for (int j = 0; j<h; j++)
		{
			x = i; y = (h - 1) - j;
			r = red[i + 1][j + 1];
			g = green[i + 1][j + 1];
			b = blue[i + 1][j + 1];
			if (r > 255) r = 255;
			if (g > 255) g = 255;
			if (b > 255) b = 255;
			img[(x + y * w) * 3 + 2] = (unsigned char)(r);
			img[(x + y * w) * 3 + 1] = (unsigned char)(g);
			img[(x + y * w) * 3 + 0] = (unsigned char)(b);
		}
	}
	cout << "Finished for loop w & h \n";
	unsigned char bmp_file_header[14] = { 'B','M', 0,0,0,0, 0,0, 0,0, 54,0,0,0 };
	unsigned char bmp_info_header[40] = { 40,0,0,0, 0,0,0,0, 0,0,0,0, 1,0, 24,0 };
	unsigned char bmppad[3] = { 0,0,0 };

	bmp_file_header[2] = (unsigned char)(filesize);
	bmp_file_header[3] = (unsigned char)(filesize >> 8);
	bmp_file_header[4] = (unsigned char)(filesize >> 16);
	bmp_file_header[5] = (unsigned char)(filesize >> 24);

	bmp_info_header[4] = (unsigned char)(w);
	bmp_info_header[5] = (unsigned char)(w >> 8);
	bmp_info_header[6] = (unsigned char)(w >> 16);
	bmp_info_header[7] = (unsigned char)(w >> 24);
	bmp_info_header[8] = (unsigned char)(h);
	bmp_info_header[9] = (unsigned char)(h >> 8);
	bmp_info_header[10] = (unsigned char)(h >> 16);
	bmp_info_header[11] = (unsigned char)(h >> 24);
	cout << "Finished bmp importing \n";
	const char name[] = "files/c.bmp";
	string fname = "files/" + z + ".bmp";
	cout << "Finished name and fname assignment \n";
	cout << fname << "\n";
	cout << "End print out fname \n";
	f = fopen(fname.c_str(), "wb");
	fwrite(bmp_file_header, 1, 14, f);
	fwrite(bmp_info_header, 1, 40, f);
	cout << "Finished fwrite \n";
	for (int i = 0; i<h; i++)
	{
		fwrite(img + (w*(h - i - 1) * 3), 3, w, f);
		fwrite(bmppad, 1, (4 - (w * 3) % 4) % 4, f);
	}

	free(img);
	fclose(f);
}
int main()
{
	//adjust nDatasize reduce traing dataset
	init_array();
	for (int i = 0; i < nDatasize; i++)
	{
		cout << i << "\n";
		reader(i, nDatasize, "t");
		rw_file(to_string(i));
	}
	return 0;
}
