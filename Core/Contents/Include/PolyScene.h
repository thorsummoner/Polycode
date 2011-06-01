/*
Copyright (C) 2011 by Ivan Safrin

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
#include "PolyString.h"
#include "PolyGlobals.h"
#include "PolyRenderer.h"
#include "PolySceneEntity.h"
#include "PolyCamera.h"
#include "PolySceneLight.h"
#include "PolySceneMesh.h"
#include <vector>

using std::vector;

namespace Polycode {
		
	class Camera;
	class SceneLight;
	class SceneMesh;
	
	/**
	* 3D rendering container. The Scene class is the main container for all 3D rendering in Polycode. Scenes are automatically rendered and need only be instantiated to immediately add themselves to the rendering pipeline. A Scene is created with a camera automatically.
	*/ 
	class _PolyExport Scene : public EventDispatcher {
	public:
		
		/**
		* Default constructor.
		*/
		Scene();
		/**
		* Default constructor with options. 
		* @param virtualScene If this flag is set to true, the scene is not rendered to the screen. Use this if you want to render the scene only to a texture.
		*/		
		Scene(bool virtualScene);
		virtual ~Scene();
		
		/**
		* Adds a new SceneEntity to the scene
		* @param entity New entity to add.
		*/
		void addEntity(SceneEntity *entity);
		
		/**
		* Removes a SceneEntity from the scene
		* @param entity New entity to remove.
		*/		
		void removeEntity(SceneEntity *entity);
		
		/**
		* Returns the scene's default camera.
		* @return The scene's default camera.
		*/				
		Camera *getDefaultCamera();
		
		/**
		* Enables and disables lighting in the scene.
		* @param enable If false, disables lighting in the scene, if true, enables it.		
		*/
		void enableLighting(bool enable);				
		
		/**
		* Enables and disables fog in the scene.
		* @param enable If false, disables lighting in the scene, if true, enables it.		
		*/		
		void enableFog(bool enable);
		
		/**
		* Sets the fog properties for the scene.
		* @param fogMode Fog falloff mode. (Renderer::FOG_LINEAR, Renderer::FOG_EXP, Renderer::FOG_EXP2).
		* @param color Fog color.
		* @param density Fog density.
		* @param startDepth Starting depth of the fog.
		* @param endDepth Ending depth of the fog.							
		*/				
		void setFogProperties(int fogMode, Color color, Number density, Number startDepth, Number endDepth);
	
		virtual void Update();
		void setVirtual(bool val);
		bool isVirtual();
	
		bool isEnabled();		
		void setEnabled(bool enabled);
		
		int getNumEntities() { return entities.size(); }
		SceneEntity *getEntity(int index) { return entities[index]; }
		
		/**
		* Returns the entity at the specified screen position. This is currently very slow and not super reliable.
		* @param x X position.
		* @param y Y position.
		* @return Entity at specified screen position.		
		*/
		SceneEntity *getEntityAtScreenPosition(Number x, Number y);
		
		void Render(Camera *targetCamera = NULL);
		void RenderDepthOnly(Camera *targetCamera);
		
		static String readString(OSFILE *inFile);
		void loadScene(String fileName);
		void generateLightmaps(Number lightMapRes, Number lightMapQuality, int numRadPasses);
		
		/**
		* Adds a light to the scene.
		* @param light Light to add to the scene.
		*/
		void addLight(SceneLight *light);
		SceneLight *getNearestLight(Vector3 pos);
		
		void writeEntityMatrix(SceneEntity *entity, OSFILE *outFile);
		void writeString(String str, OSFILE *outFile);
		void saveScene(String fileName);
		
		int getNumStaticGeometry();
		SceneMesh *getStaticGeometry(int index);
		
		virtual void loadCollisionChild(SceneEntity *entity, bool autoCollide=false, int type=0){}
		
		int getNumLights();
		SceneLight *getLight(int index);
		
		SceneEntity *getCustomEntityByType(String type);
		vector<SceneEntity*> getCustomEntitiesByType(String type);		
		
		static const unsigned int ENTITY_MESH = 0;
		static const unsigned int ENTITY_LIGHT = 1;			
		static const unsigned int ENTITY_CAMERA = 2;			
		static const unsigned int ENTITY_ENTITY = 3;
		static const unsigned int ENTITY_COLLMESH = 4;
		
		/**
		* Scene clear color
		*/ 
		Color clearColor;
		
		/**
		* If set to true, the renderer will use the scene's clear color when rendering the scene.
		*/
		bool useClearColor;

		/**
		* Ambient color, passed to lighting shaders
		*/				
		Color ambientColor;		
		
		/**
		* Fog color, passed to lighting shaders.
		*/						
		Color fogColor;				
		
		/**
		* If this is set to false, the scene is not rendered or updated during the render loop.
		*/
		bool enabled;		
		
	protected:
		
		bool hasLightmaps;
		
		vector <SceneLight*> lights;				
		vector <SceneMesh*> staticGeometry;
		vector <SceneMesh*> collisionGeometry;
		vector <SceneEntity*> customEntities;
		
		
		bool isSceneVirtual;
		
		Camera *defaultCamera;
		vector <SceneEntity*> entities;
		
		bool lightingEnabled;
		bool fogEnabled;
		int fogMode;
		Number fogDensity;
		Number fogStartDepth;
		Number fogEndDepth;
		
	};
}