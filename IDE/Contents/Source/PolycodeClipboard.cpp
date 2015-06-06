
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

#include "PolycodeClipboard.h"

PolycodeClipboard::PolycodeClipboard() {
	data = NULL;
}

void PolycodeClipboard::setData(void *data, String type, ClipboardProvider *provider) {
	if(!data)
		return;

	if(this->data && currentProvider) {
		currentProvider->destroyClipboardData(this->data, this->type);
		this->data = NULL;
		currentProvider = NULL;
	}
	
	this->data = data;
	this->type = type;
	currentProvider = provider;
}

ClipboardProvider *PolycodeClipboard::getCurrentProvider() {
    return currentProvider;
}

void PolycodeClipboard::setCurrentProvider(ClipboardProvider *provider) {
    currentProvider = provider;
}

void *PolycodeClipboard::getData() {
	return data;
}

String PolycodeClipboard::getType() {
	return type;
}
