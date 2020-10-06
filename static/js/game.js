function clickShowPositionBtn () {
  console.log('Current position as an Object:')
  console.log(board.position())

  console.log('Current position as a FEN string:')
  console.log(board.fen())
}

function savePosition () {
    var txt=document.getElementById("position").value;
    txt=txt + board.fen();
    document.getElementById("position").value=txt;
}

function saveFile() {
    var txt=document.getElementById("position").value;
    txt=board.fen();

    $.post( "/postmethod", {
      fen_data: JSON.stringify(txt)
    }, function(err, req, resp){
      txt= resp["responseJSON"]["fen"];
      document.getElementById("position").value=txt;
    });
}

function loadPosition() {
   var txt=document.getElementById("position").value;
   var url='/getFenPosition/'+txt;
   fetch(url).then(function(response) {
      return response.json();
   }).then(function(response) {
      var mydata = response['data'].replace(/\n/g,'');
      this.board.position(mydata);
      console.log(mydata);
   });
}

function clearPosition() {
      document.getElementById("position").value="";
}

function readPosition() {
    var txt=document.getElementById("position").value;
    newWindow=window.open("/getPosition/"+txt,"_blank", "toolbar=no,scrollbars=no,resizable=no,top=500,left=500,width=800,height=400")
}

function analyzePosition() {
    var txt=document.getElementById("position").value;
    newWindow=window.open("/getAnalitics/"+txt,"_blank", "toolbar=no,scrollbars=no,resizable=no,top=500,left=500,width=480,height=480")
}

var board = Chessboard('myBoard', {
  draggable: true,
  dropOffBoard: 'trash',
  onDragStart: true,
  sparePieces: true
})

$('#startBtn').on('click', board.start)
$('#flipOrientationBtn').on('click', board.flip)
$('#clearBtn').on('click', board.clear)
$('#saveBtn').on('click', saveFile)
$('#readBtn').on('click', readPosition)
$('#loadBtn').on('click', loadPosition)
$('#anaBtn').on('click', analyzePosition)
