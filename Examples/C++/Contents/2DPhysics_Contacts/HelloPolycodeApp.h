#include <Polycode.h>
#include "PolycodeView.h"
#include "Polycode2DPhysics.h"

using namespace Polycode;

class HelloPolycodeApp : public EventHandler {
public:
    HelloPolycodeApp(PolycodeView *view);
    ~HelloPolycodeApp();    
    bool Update();
	
	void handleEvent(Event *e);
    
private:
    Core *core;	
	Sound *collisionSound;
	PhysicsScene2D *scene;	
};