/*
 * SolLewittSvg
 *
 * For course: https://www.freecodecamp.org/news/data-visualizatoin-with-d3/
 *
 * Uses JS Class template:
 * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes
 */

SVG_NS_URL = 'http://www.w3.org/2000/svg'

class SolLewittSvg {
  constructor() {
  }

  /*
   * Static Methods
  **/
  static circler(parentId) {
    const parent = document.getElementById(parentId)

    // Artwork parameters
    const canvasWidth = 400
    const canvasHeight = 400
    const numCircles = 50
    const startRadius = 4
    const angleStep = 360.0 / numCircles
    const centerX = canvasWidth / 2
    const centerY = canvasHeight / 2

    // Create SVG and append to parent element
    const sol = new SolLewittSvg()
    const artSvg = sol.createSvgEl('svg', {width: canvasWidth, height: canvasHeight})
    parent.appendChild(artSvg)

    for (let n=0; n <= numCircles; n++) {
      if ( n > 16000 ) {
        throw "Stop before you run out of memory!"
      }

      let angle = angleStep * n
      let radius = startRadius * n
      let cx = centerX + (radius * Math.cos( angle ))
      let cy = centerY + (radius * Math.sin( angle ))
      let fill = n % 2 == 0 ? 'black' : 'white'
      let stroke = n % 2 == 1 ? 'white' : 'black'
      let opacity = 1.0 - (n / numCircles)
      //console.log(radius, [cx, cy], fill, opacity)
      let nextCircle = sol.createCircle(
        radius,
        cx,
        cy,
        {fill: fill, stroke: 'transparent'}
      )
      nextCircle.style.opacity = opacity
      artSvg.append(nextCircle)
    }
  }

  static reproduce(parentId) {
    const canvasWidth = 400
    const canvasHeight = 400
    const parent = document.getElementById(parentId)

    // Create SVG and append to parent element
    const sol = new SolLewittSvg()

    // Create background SVG: rows
    const bgSvg = sol.createSvgEl('svg', {width: canvasWidth, height: canvasHeight})

    const rowHeight = 10
    const numRows = canvasHeight / rowHeight
    for (let i = 0; i < numRows; i++) {
      let fillColor = i % 2 == 0 ? 'black' : 'white'
      let y = i * 10
      let row = sol.createRect(canvasWidth, rowHeight, 0, y, {fill: fillColor})
      bgSvg.appendChild(row)
    }

    parent.appendChild(bgSvg)

    // Create foreground SVG: columns in circle
    const circleRadius = canvasHeight / 3
    const fgSvg = sol.createSvgEl('svg', {
      width: canvasWidth,
      height: canvasHeight
    })
    fgSvg.style.position = 'absolute'
    fgSvg.style.top = `${(canvasHeight / 2) - circleRadius}px`
    fgSvg.style.left = '0px'

    const colWidth = 10
    const numCols = canvasWidth / colWidth
    for (let i = 0; i < numCols; i++) {
      let fillColor = i % 2 == 0 ? 'black' : 'white'
      let x = i * 10
      let col = sol.createRect(colWidth, canvasHeight, x, 0, {fill: fillColor})
      fgSvg.appendChild(col)
    }

    parent.appendChild(fgSvg)

    // Create column mask: cut out columns in circle
    const colMask = sol.createSvgEl('mask')
    colMask.setAttribute('id', 'col-mask')
    fgSvg.appendChild(colMask)

    const colMaskRect = sol.createSvgEl('rect')
    colMaskRect.setAttribute('width', canvasWidth)
    colMaskRect.setAttribute('height', canvasHeight)
    colMaskRect.setAttribute('fill', 'black')
    colMask.append(colMaskRect)

    const colMaskCircle = sol.createCircle(
      circleRadius,
      canvasWidth / 2,
      canvasHeight / 2,
      {fill: 'white'}
    )
    colMask.append(colMaskCircle)

    fgSvg.setAttribute('mask', 'url(#col-mask)')
  }

  /*
   * Getters
  **/

  /*
   * Methods
  **/
  createSvgEl(el, attrs) {
    attrs = attrs !== undefined ? attrs : {}
    const svg = document.createElementNS(SVG_NS_URL, el)
    for (const [attr, value] of Object.entries(attrs)) {
      svg.setAttribute(attr, value)
    }
    return svg
  }

  createRect(width, height, x, y, attrs) {
    const rectAttrs = {
      width: width,
      height: height,
      x: x,
      y: y
    }
    const elAttrs = Object.assign(rectAttrs, attrs)
    return this.createSvgEl('rect', elAttrs)
  }

  createCircle(r, cx, cy, attrs) {
    const rectAttrs = {
      r: r,
      cx: cx,
      cy: cy
    }
    const elAttrs = Object.assign(rectAttrs, attrs)
    return this.createSvgEl('circle', elAttrs)
  }

  createMask(el, id) {
    const attrs = {
      id: id,
      'data-url': `url(#${id})`
    }
    return this.createSvgEl('mask', attrs)
  }
}
