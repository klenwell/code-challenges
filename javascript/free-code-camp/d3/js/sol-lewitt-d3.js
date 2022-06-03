/*
 * SolLewittSvg
 *
 * For course: https://www.freecodecamp.org/news/data-visualizatoin-with-d3/
 *
 * Uses JS Class template:
 * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes
**/


SVG_NS_URL = 'http://www.w3.org/2000/svg'


class SolLewittD3 {
  constructor() {
  }

  /*
   * Static Methods
  **/
  static circle(parentId) {
    const canvasWidth = 400
    const canvasHeight = 400
    const parent = d3.select(`#${parentId}`)

    // Create SVG
    const svg = parent
      .append('svg')
      .attr('width', canvasWidth)
      .attr('height', canvasHeight)

    // Create SVG background: columns
    const colWidth = 10
    const numCols = canvasWidth / colWidth
    svg.selectAll('rect')
      .data(d3.range(numCols))
      .join('rect')
      .attr('x', (n) => n * 10)
      .attr('y', 0)
      .attr('width', colWidth)
      .attr('height', canvasHeight)
      .attr('fill', (n) => n % 2 == 0 ? 'black' : 'white')

    // Create SVG foreground: columns in circle
    const circleRadius = canvasHeight / 3
    const rowHeight = 10
    const numRows = canvasHeight / rowHeight
    const posLeft = 0
    const posTop = (canvasHeight / 2) - circleRadius
    const styleAttr = `position: absolute; left: ${posLeft}px; top: ${posTop}px`
    const fgSvg = parent
      .append('svg')
      .attr('width', canvasWidth)
      .attr('height', canvasHeight)
      .attr('style', styleAttr)

    fgSvg.selectAll('rect')
      .data(d3.range(numRows))
      .join('rect')
      .attr('y', (n) => n * 10)
      .attr('width', canvasWidth)
      .attr('height', rowHeight)
      .attr('fill', (n) => n % 2 == 0 ? 'black' : 'white')

    // Create column mask: cut out columns in circle
    const colMaskId = 'col-mask'
    const colMask = fgSvg.append('mask').attr('id', colMaskId)
    const colMaskRect = colMask.append('rect')
      .attr('width', canvasWidth)
      .attr('height', canvasHeight)
      .attr('fill', 'black')
    const colMaskCircle = colMask.append('circle')
      .attr('r', circleRadius)
      .attr('cx', canvasWidth / 2)
      .attr('cy', canvasHeight / 2)
      .attr('fill', 'white')

    // Apply mask
    fgSvg.attr('mask', `url(#${colMaskId})`)
  }

  /*
   * Getters
  **/

  /*
   * Methods
  **/
}
