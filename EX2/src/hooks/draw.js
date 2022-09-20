function drawConcentricCircle(canvas, positionX, positionY, color) {
  const ctx = canvas.getContext("2d");
  ctx.save()
  ctx.beginPath();
  ctx.arc(positionX, positionY, 15, 0, 2 * Math.PI);
  ctx.fillStyle = 'black'
  ctx.fill()
  ctx.stroke()
  ctx.closePath()

  ctx.beginPath()
  ctx.arc(positionX, positionY, 11, 0, 2 * Math.PI);
  ctx.fillStyle = color
  ctx.fill()
  ctx.stroke();
  ctx.restore()
}
function drawLine(canvas, fromPositionX, fromPositionY, ToPositionX, ToPositionY) {
  const ctx = canvas.getContext("2d");
  ctx.save();
  ctx.beginPath();
  ctx.lineWidth = 5;
  ctx.lineCap = 'round';
  ctx.moveTo(fromPositionX, fromPositionY);
  ctx.lineTo(ToPositionX, ToPositionY);
  ctx.stroke()
  ctx.restore()
}

export { drawConcentricCircle, drawLine }