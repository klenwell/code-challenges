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
  constructor(parentSel, canvasWidth, canvasHeight) {
    this.parentSel = parentSel
    this.canvasWidth = 400
    this.canvasHeight = 400
    this.parent = d3.select(parentSel)
    console.log(this.parent)
  }

  /*
   * Static Methods
  **/
  renderCircle() {
    const circleRadius = this.canvasHeight / 3

    // Create SVG background: columns
    const bgSvg = this.appendBgAsColumns()

    // Create SVG foreground: rows in circle
    const fgSvg = this.appendBgAsRows()
    const posLeft = 0
    const posTop = 0
    const styleAttr = `position: absolute; left: ${posLeft}px; top: ${posTop}px`
    fgSvg.attr('style', styleAttr)

    // Create column mask: cut out columns in circle
    const fgMaskId = 'col-mask'
    const fgMask = fgSvg.append('mask').attr('id', fgMaskId)
    const fgMaskRect = fgMask.append('rect')
      .attr('width', this.canvasWidth)
      .attr('height', this.canvasHeight)
      .attr('fill', 'black')
    const fgMaskCircle = fgMask.append('circle')
      .attr('r', circleRadius)
      .attr('cx', this.canvasWidth / 2)
      .attr('cy', this.canvasHeight / 2)
      .attr('fill', 'white')

    // Apply mask
    fgSvg.attr('mask', `url(#${fgMaskId})`)
  }

  renderTriangle() {
    const fgMaskId = 'fg-triangle-mask'

    // Create SVG background: columns
    const bgSvg = this.appendBgAsColumns()

    // Create SVG foreground: rows in circle
    const fgSvg = this.appendBgAsRows()
    const posLeft = this.canvasWidth
    const posTop = 0
    const styleAttr = `position: absolute; left: ${posLeft}px; top: ${posTop}px`
    fgSvg.attr('style', styleAttr)

    // Create column mask: cut out columns in circle
    const fgMask = fgSvg.append('mask').attr('id', fgMaskId)
    fgMask
      .append('rect')
      .attr('width', this.canvasWidth)
      .attr('height', this.canvasHeight)
      .attr('fill', 'black')

    const dSymbol = d3.symbol(d3.symbols[1], 40000)
    fgMask
      .append('g')
      .attr('transform', `translate(200, 200)`)
      .append('path')
      .attr('d', dSymbol())
      .attr('fill', 'white')

    // Apply mask
    fgSvg.attr('mask', `url(#${fgMaskId})`)
  }

  appendBgAsColumns() {
    const colWidth = 10
    const numCols = this.canvasWidth / colWidth

    const svg = this.parent
      .append('svg')
      .attr('width', this.canvasWidth)
      .attr('height', this.canvasHeight)

    svg.selectAll('rect')
      .data(d3.range(numCols))
      .join('rect')
      .attr('x', (n) => n * 10)
      .attr('y', 0)
      .attr('width', colWidth)
      .attr('height', this.canvasHeight)
      .attr('fill', (n) => n % 2 == 0 ? 'black' : 'white')

    return svg
  }

  appendBgAsRows() {
    const rowHeight = 10
    const numRows = this.canvasHeight / rowHeight

    const svg = this.parent
      .append('svg')
      .attr('width', this.canvasWidth)
      .attr('height', this.canvasHeight)

    svg.selectAll('rect')
      .data(d3.range(numRows))
      .join('rect')
      .attr('y', (n) => n * 10)
      .attr('width', this.canvasWidth)
      .attr('height', rowHeight)
      .attr('fill', (n) => n % 2 == 0 ? 'black' : 'white')

    return svg
  }

  /*
   * Getters
  **/

  /*
   * Methods
  **/
}
