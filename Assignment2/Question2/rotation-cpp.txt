#include <GL/glut.h>
#include <vector>

struct Point {
	float x, y;
};


//an example of a concave polygon (having an arrow shape)
std::vector<Point> polygon = {
	{100, 300},
	{200, 400},
	{300, 300},
	{250, 250},
	{200, 270},
	{150, 250},
};


void drawPolygon(const std::vector<Point>& poly, float r, float g, float b) {
	glColor3f(r, g, b);
	glBegin(GL_POLYGON);
	for (const auto& p : poly) {
		glVertex2f(p.x, p.y);
	}
	glEnd();
}


//splitting the function using rotational idea
void splitConcavePolygon() {
	glClear(GL_COLOR_BUFFER_BIT);

	//Drawing the original polygon
	drawPolygon(polygon, 0.8f, 0.8f, 0.8f);

	//finding a reflec vertex manually (point 3: index 3)
	//then we will split from point 3 to point 0 for simplicity (valid split)
	Point splitStart = polygon[3];
	Point splitEnd = polygon[0];

	//Drawing the splitting line
	glColor3f(1, 0, 0);
	glLineWidth(2);
	glBegin(GL_LINES);
	glVertex2f(splitStart.x, splitStart.y);
	glVertex2f(splitEnd.x, splitEnd.y);
	glEnd();


	//Defining the two new polygons
	std::vector<Point> poly1 = {
		polygon[0], polygon[1], polygon[2], polygon[3]
	};

	std::vector<Point> poly2 = {
		polygon[3], polygon[4], polygon[5], polygon[0]
	};


	//Drawing the sub-polygons
	drawPolygon(poly1, 0.2f, 0.8f, 0.2f); //greenish
	drawPolygon(poly2, 0.2f, 0.2f, 0.8f); //blueish

	glFlush();
}

void init() {
	glClearColor(1.0, 1.0, 1.0, 1.0); //white background
	glMatrixMode(GL_PROJECTION);
	gluOrtho2D(0, 500, 0, 500);
}

int main(int argc, char** argv) {
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
	glutInitWindowSize(600, 600);
	glutInitWindowPosition(100, 100);
	glutCreateWindow("Concave Polygon Split - Rotational Method");

	init();
	glutDisplayFunc(splitConcavePolygon);
	glutMainLoop();
	return 0;
}
