export default function drawConcentricCircle(canvas, positionX, positionY, color) {
  const ctx = canvas.getContext("2d");
  ctx.beginPath();
  ctx.arc(positionX, positionY, 15, 0, 2 * Math.PI);
  ctx.fillStyle = 'black'
  ctx.fill()
  ctx.stroke()
  ctx.closePath()

  ctx.beginPath()
  ctx.arc(positionX, positionY, 10, 0, 2 * Math.PI);
  ctx.fillStyle = color
  ctx.fill()
  ctx.stroke();
}