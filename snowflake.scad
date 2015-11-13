module hook() {
  translate([30, 18, 0])
  difference() {
    circle(6);
    circle(5);
  }
}

linear_extrude(height = 1, center = true, convexity = 10, twist = 0)
union() {
  hook();
  scale([5, 5, 0]) 
  difference() {
  polygon(points=k3);
  translate([3, -1.1, 0]) scale([0.5, 0.5, 0.5]) polygon(points=k2);
  }
}
