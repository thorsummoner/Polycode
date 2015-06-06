/*
 Copyright (C) 2012 by Ivan Safrin
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.
 */
 
#pragma once

#include "PolycodeProject.h"
#include "PolycodeConsole.h"

class PolycodeRunner : public Threaded {
	public:
		PolycodeRunner(String polyappPath);
		
		void runThread();
		
		String polyappPath;
};

class GenericRunner : public Threaded {
	public:
		GenericRunner(String app, String file, String inFolder);
		
		void runThread();
		
		String app;
		String file;	
		String inFolder;	
};

class PolycodeToolLauncher {
	public: 
		PolycodeToolLauncher();
		~PolycodeToolLauncher();		
		
		static void openExternalEditor(String app, String file, String inFolder);
		static String generateTempPath(PolycodeProject *project);
		static void buildProject(PolycodeProject *project, String destinationPath, bool compileScripts);
		static String importAssets(String sourceFile, String inFolder, bool addMeshes, String prefix, bool swapZY, bool generateNormals, bool generateTangents, bool listOnly,bool writeNormals, bool writeTangents, bool writeColors, bool writeBoneWeights, bool writeUVs, bool writeSecondaryUVs, bool exportScene, bool generateMaterialFile, bool overrideMaterials, String materialOverrideName, bool specifyBaseAssetPath, String baseAssetPath);

		static void runPolyapp(String polyappPath);
};