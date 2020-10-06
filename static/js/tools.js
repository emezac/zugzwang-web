// Only executed our code once the DOM is ready.
	window.onload = function() {
/* Arrow Class extends Group */

const Arrow = paper.Group.extend({
  initialize: function (args) {
    paper.Group.call(this, args)
    this._class = 'Arrow'
    this._serializeFields = Object.assign(this._serializeFields, {
      from: null,
      to: null,
      headSize: null
    })

    this.from = args.from
    this.to = args.to || args.from
    this.headSize = args.headSize

    // @NOTE
    // `paper.project.importJSON()` passes the deserialized children
    // (the arrow parts) to the `Group` superclass so there's no need to
    // create them again.
    if (this.children.length)
      return

    this.addChildren([
      new paper.Path({
        ...args,
        segments: [
          this.from,
          this.from
        ]
      }),
      new paper.Path({
        ...args,
        segments: [
          this.from,
          this.from
        ]
      }),
      new paper.Path({
        ...args,
        segments: [
          this.from,
          this.from
        ]
      })
    ])

    this.update(this.to)
  },

  update: function (point) {
    const angle = this.from.subtract(point).angle - 90

    this.children[0].lastSegment.point = point

    this.children[1].firstSegment.point = point
    this.children[1].lastSegment.point = point.add(
      this.headSize,
      this.headSize
    )

    this.children[2].firstSegment.point = point
    this.children[2].lastSegment.point = point.add(
      -this.headSize,
      this.headSize
    )

    this.children[1].rotate(angle, point)
    this.children[2].rotate(angle, point)

    return this
  }
})
			// Setup Paper

  paper.Base.exports.Arrow = Arrow
  paper.setup(document.querySelector('canvas'))

  // Toolstack

  class ToolStack {
    constructor(tools) {
      this.tools = tools.map(tool => tool())
    }

    activateTool(name) {
      const tool = this.tools.find(tool => tool.name === name)
      tool.activate()
    }

    // add more methods here as you see fit ...
  }



/* Usage */


  // Tool Red Arrow, draws paths on mouse-drag

  const toolRed = () => {
    const tool = new paper.Tool()
    tool.name = 'toolRedArrow'

    let arrow

    tool.onMouseDown = e => {
     arrow = new Arrow({
      from: e.point,
      headSize: 10,
      strokeWidth: 2.5,
      strokeColor: '#DC143C',
      strokeCap: 'round'
    })
    }

   tool.onMouseDrag = e => {
     arrow.update(e.point)
    }

    return tool
  }

  // Tool Green Arrow
  const toolGreen= () => {
    const tool = new paper.Tool()
    tool.name = 'toolGreenArrow'

    let arrow

    tool.onMouseDown = e => {
     arrow = new Arrow({
      from: e.point,
      headSize: 10,
      strokeWidth: 2.5,
      strokeColor: '#008000',
      strokeCap: 'round'
    })
    }

   tool.onMouseDrag = e => {
     arrow.update(e.point)
    }

    return tool
  }

  // Tool Yellow Arrow
  const toolYellow = () => {
    const tool = new paper.Tool()
    tool.name = 'toolYellowArrow'

    let arrow

    tool.onMouseDown = e => {
     arrow = new Arrow({
      from: e.point,
      headSize: 10,
      strokeWidth: 2.5,
      strokeColor: '#CCCC00',
      strokeCap: 'round'
    })
    }

   tool.onMouseDrag = e => {
     arrow.update(e.point)
    }

    return tool
  }

  const toolCircle = () => {
    const tool = new paper.Tool()
    tool.name = 'toolCircle'

    let path

    tool.onMouseDown = e => {
     path = new paper.Path.Circle({
        center: e.point,
        strokeWidth: 1.5,
        radius: 24,
        strokeColor: '#1E90FF',
     })
    }
    return tool
  }

  const toolSquare = () => {
    const tool = new paper.Tool()
    tool.name = 'toolSquare'

    let path

    tool.onMouseDown = e => {
     path = new paper.Path.Rectangle({
        point: e.point,
        size: {width:  47, height: 47}  ,
        strokeWidth: 4.5,
        strokeColor: '#20B2AA',
     })
    }
    return tool
  }

  const toolCross = () => {
    const tool = new paper.Tool()
    tool.name = 'toolCross'

    let path

    tool.onMouseDown = e => {
    var text = new paper.PointText({
        point: e.point,
        content: 'X',
        fillColor: 'black',
        fontFamily: 'Courier New',
        fontWeight: 'bold',
        fontSize: 65
     });
    }
    return tool
  }

  const toolAster = () => {
    const tool = new paper.Tool()
    tool.name = 'toolAster'

    let path

    tool.onMouseDown = e => {
    var text = new paper.PointText({
        point: e.point,
        content: '@',
        fillColor: 'black',
        fontFamily: 'Arial',
        fontWeight: 'bold',
        fontSize: 65
     });
    }
    return tool
  }

  const toolFCircle = () => {
    const tool = new paper.Tool()
    tool.name = 'toolFCircle'

    let path

    tool.onMouseDown = e => {
      path = new paper.Path.Circle({
        center: e.point,
        radius: 24,
        fillColor: 'black'
      })
    }
    return tool
  }

  // Construct a Toolstack, passing your Tools

  const toolStack = new ToolStack([toolRed, toolYellow, toolGreen, toolCircle, toolSquare, toolCross, toolFCircle])

  // Activate a certain Tool

  toolStack.activateTool('toolRedArrow')

  // Attach click handlers for Tool activation on all
  // DOM buttons with class '.tool-button'

  document.querySelectorAll('.tool-button').forEach(toolBtn => {
    toolBtn.addEventListener('click', e => {
      toolStack.activateTool(e.target.getAttribute('data-tool-name'))
    })
  })
	}
