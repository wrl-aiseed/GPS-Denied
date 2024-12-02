# cifar-10 reader and visulizer in c++

First download the cifar-10 database and add them to the directory of the .exe

If VS throws a -d-scl-secure-no-warnings; 
Then ensure that you #pragma warning(disable:4996) or _SCL_SECURE_NO_WARNINGS , you can find 
_SCL_SECURE_NO_WARNINGS in solution explorer, right click the project, select "properties".
Expand the ">C/C++" entry in the tree and select "Preprocessor" under that. 
In that edit box, add _SCL_SECURE_NO_WARNINGS, separating it from the other entries with a ; 

Also when you compile with cl.exe /EHsc /W4 /MTd file-name.cpp the 
compiler emits a warning, but compiles without error into an executable:

## Why?

This project exist to aid any develover who aims to view the cifar-10 database , 
it's a simple project with little overhead and run effiently .



## Usage

Here is a simple usage of the function.

Just subsititute the nDatasize to adjust how much data you want to view .
Ensure you create a folder which will store the visualized/render data .

```bash


	//adjust nDatasize reduce training dataset
	for (int i = 0; i < nDatasize; i++)
	{
		reader(i, nDatasize, "t");
		rw_file(to_string(i));
	}

```
```bash

External libraries or OpenCV not required .

```

## License

The header files are distributed under the terms of the MIT License. The
CIFAR-10 are not my property. If used in a paper, you'll need to cite the reference
paper, as indicated in the `official website <https://www.cs.toronto.edu/~kriz/cifar.html>`_.
