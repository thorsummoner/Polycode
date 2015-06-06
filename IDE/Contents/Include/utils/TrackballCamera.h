/*
 Copyright (C) 2013 by Ivan Safrin
 
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

#include "Polycode.h"
#include "OSBasics.h"

using namespace Polycode;

class TrackballCamera : public EventHandler {
	public:
		TrackballCamera(Camera *targetCamera, Entity *trackballShape);
		~TrackballCamera();
		
		void handleEvent(Event *event);		
		void setOrbitingCenter(const Vector3 &newCenter);
		void setCameraDistance(Number cameraDistance);
		Camera *getTargetCamera();
		
		static const int MOUSE_MODE_IDLE = 0;
		static const int MOUSE_MODE_ORBITING = 1;
		static const int MOUSE_MODE_PANNING = 2;
		static const int MOUSE_MODE_ZOOMING = 3;				
		
		Number trackballPanSpeed;
		Number trackballZoomSpeed;	
		Number trackballRotateSpeed;
		
	private:
	
		int mouseMode;
	
		Vector3 getMouseProjectionOnBall(const Vector2 &mousePosition);
		void updateCamera();	
		void processMouseMovement(const Vector2 &newPosition);
		
		Camera *targetCamera;
		Entity *trackballShape;
		
		Vector2 trackBallMouseStart;
		Vector2 trackBallMouseEnd;			
		Vector3 orbitingCenter;
		Vector3 trackballRotateStart;
		Vector3 trackballRotateEnd;	
		Vector3 trackballEye;		
		Number cameraDistance;
		CoreInput *coreInput;		
		
};
