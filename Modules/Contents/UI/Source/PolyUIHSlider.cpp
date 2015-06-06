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


#include "PolyUIHSlider.h"
#include "PolyConfig.h"
#include "PolyCoreServices.h"

using namespace Polycode;

UIHSlider::UIHSlider(Number start, Number end, Number width) : UIElement() {

	continuous = true;
	
	Config *conf = CoreServices::getInstance()->getConfig();	
    Number uiScale = conf->getNumericValue("Polycode", "uiScale");
	
	String bgImage = conf->getStringValue("Polycode", "uiHSliderBg");
	String gripImage = conf->getStringValue("Polycode", "uiHSliderGrip");	
	bgHeight = conf->getNumericValue("Polycode", "uiHSliderBgHeight");

    sidePadding = conf->getNumericValue("Polycode", "uiHSliderSidePadding");
    
	Number st = conf->getNumericValue("Polycode", "uiHSliderBgT");
	Number sr = conf->getNumericValue("Polycode", "uiHSliderBgR");
	Number sb = conf->getNumericValue("Polycode", "uiHSliderBgB");
	Number sl = conf->getNumericValue("Polycode", "uiHSliderBgL");
	

	bgRect = new UIBox(bgImage, st, sr, sb, sl, width, bgHeight);
	addChild(bgRect);
	
	sliderWidth = width - (sidePadding*2);
	
	sliderValue = start;
	startValue = start;
	endValue = end;
		
	gripRect = new UIImage(gripImage);
    gripRect->Resize(gripRect->getWidth() / uiScale, gripRect->getHeight() / uiScale);
	gripRect->setAnchorPoint(0.0, 0.0, 0.0);
	gripRect->setPosition(0, floor(bgHeight/2.0));

	bgHitBox = new Entity();
    bgHitBox->setWidth(width);
    bgHitBox->setHeight(gripRect->getHeight());
    bgHitBox->visible = false;
	bgHitBox->setAnchorPoint(-1.0, -1.0, 0.0);
	bgHitBox->setPosition(0, gripRect->getPosition().y - (gripRect->getHeight()/2.0));
	addChild(bgHitBox);

	addChild(gripRect);

	bgHitBox->addEventListener(this, InputEvent::EVENT_MOUSEUP);
	bgHitBox->addEventListener(this, InputEvent::EVENT_MOUSEUP_OUTSIDE);
	bgHitBox->addEventListener(this, InputEvent::EVENT_MOUSEDOWN);
	bgHitBox->processInputEvents = true;

	gripRect->addEventListener(this, InputEvent::EVENT_MOUSEUP);
	gripRect->addEventListener(this, InputEvent::EVENT_MOUSEUP_OUTSIDE);
	gripRect->addEventListener(this, InputEvent::EVENT_MOUSEDOWN);
	gripRect->processInputEvents = true;
		
	gripRect->setDragLimits(Rectangle(sidePadding,floor(bgHeight/2.0),sliderWidth,0));
	
	gripPos = sidePadding;
	dragging = false;
}

UIHSlider::~UIHSlider() {
	if(!ownsChildren) {
		delete bgRect;
		delete gripRect;
		delete bgHitBox;
	}
}

void UIHSlider::setSliderValue(Number val) {
	if(val >= startValue && val <= endValue) {
		gripRect->setPositionX(sidePadding+ (sliderWidth * ((val-startValue)/(endValue-startValue))));
		gripPos = gripRect->getPosition().x;
		sliderValue = val;
	}
}

bool UIHSlider::isContinuous() {
	return continuous;
}
void UIHSlider::setContinuous(bool _continuous) {
	continuous = _continuous;
}

Number UIHSlider::getSliderValue() {
	return sliderValue;
}

void UIHSlider::Resize(Number width, Number height) {
	bgRect->resizeBox(width, bgHeight);
	setWidth(width);
	setHeight(height);
	matrixDirty = true;	
	sliderWidth = width- (sidePadding*2);
	gripRect->setDragLimits(Rectangle(sidePadding,floor(bgHeight/2.0),sliderWidth,0));
	setSliderValue(sliderValue);
	bgHitBox->setWidth(width);
    bgHitBox->setHeight(gripRect->getHeight());
}
			
void UIHSlider::handleEvent(Event *event) {

	if(event->getDispatcher() == bgHitBox) {
		InputEvent *inputEvent = (InputEvent*)event;	
		switch(event->getEventCode()) {
			case InputEvent::EVENT_MOUSEDOWN:
				gripRect->setPositionX(inputEvent->mousePosition.x);
				gripPos = gripRect->getPosition().x;				
				sliderValue = startValue+((endValue - startValue) * ((gripPos-sidePadding)/sliderWidth));
				gripRect->startDrag(inputEvent->mousePosition.x-gripRect->getPosition().x,inputEvent->mousePosition.y-gripRect->getPosition().y);
				dragging = true;
			break;
			case InputEvent::EVENT_MOUSEUP:
			case InputEvent::EVENT_MOUSEUP_OUTSIDE:
				gripRect->stopDrag();
				if(dragging) {
					dispatchEvent(new UIEvent(), UIEvent::CHANGE_EVENT);
				}
				dragging = false;				
			break;
		}	
	}

	if(event->getDispatcher() == gripRect) {
		InputEvent *inputEvent = (InputEvent*)event;
		switch(event->getEventCode()) {
			case InputEvent::EVENT_MOUSEDOWN:			
				gripRect->startDrag(inputEvent->mousePosition.x,inputEvent->mousePosition.y);
				dragging = true;				
			break;
			case InputEvent::EVENT_MOUSEUP:
			case InputEvent::EVENT_MOUSEUP_OUTSIDE:		
				gripRect->stopDrag();
				if(dragging) {
					dispatchEvent(new UIEvent(), UIEvent::CHANGE_EVENT);
				}
				dragging = false;				
			break;
		}	
	}
}


void UIHSlider::Update() {
	if(gripRect->getPosition().x != gripPos) {
		gripPos = gripRect->getPosition().x;
		sliderValue = startValue+((endValue - startValue) * ((gripPos-sidePadding)/sliderWidth));
		if (continuous) {
			dispatchEvent(new UIEvent(), UIEvent::CHANGE_EVENT);
		}
	}
}
