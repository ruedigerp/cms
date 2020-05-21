// Main.js from FE
/**
 * Saving button
 */
const saveButton = document.getElementById('saveButton');

/**
 * To initialize the Editor, create a new instance with configuration object
 * @see docs/installation.md for mode details
 */

 function findGetParameter(parameterName) {
     var result = null,
         tmp = [];
     location.search
         .substr(1)
         .split("&")
         .forEach(function (item) {
           tmp = item.split("=");
           if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
         });
     return result;
 }

$("#saved").delay(1).fadeOut(1);

let path = location.pathname.substring(1);
let parts = window.location.pathname.split( '/' );
console.log("Part1: " + parts[3] );
let url = '/api/v1/articles/' + parts[3];
async function fetchData() {
  return fetch(url)
    .then(data => {return data.json() })
    .then(res => { createEditor(res) })
}

fetchData()

function setTitle(data) {
  document.title = data['title'];
  console.log("setTitle: " + data['title']);
  $("#documentName").text(data['title']);
}
async function fetchMeta() {
  let parts = window.location.pathname.split( '/' );
  let url = '/api/v1/metadata/' + parts[3];
  return fetch(url)
    .then(data => {return data.json() })
    .then(res => { setTitle(res) })
}
fetchMeta()

function createEditor(data){
  var editor = new EditorJS({
    /**
     * Wrapper of Editor
     */
    holder: 'editorjs',
    placeholder: '... schreibe los ...',
    autofocus: true,
    /**
     * Tools list
     */
    tools: {
      /**
       * Each Tool is a Plugin. Pass them via 'class' option with necessary settings {@link docs/tools.md}
       */
      images: SimpleImage,
      // image: {
      //   class: SimpleImage,
      //   inlineToolbar: ["link"],
      //   shortcut: 'CMD+SHIFT+J'
      // },
      header: {
        class: Header,
        inlineToolbar: ['link'],
        config: {
          placeholder: 'Header'
        },
        shortcut: 'CMD+SHIFT+H'
      },

      /**
       * Or pass class directly without any configuration
       */
      // image: SimpleImage,
      // image: {
      //   class: ImageTool,
      //   config: {
      //     endpoints: {
      //       byFile: 'http://localhost:8008/uploadFile', // Your backend file uploader endpoint
      //       byUrl: 'http://localhost:8008/fetchUrl' // Your endpoint that provides uploading by Url
      //     }
      //   }
      // },

      list: {
        class: List,
        inlineToolbar: true,
        shortcut: 'CMD+SHIFT+L'
      },

      checklist: {
        class: Checklist,
        inlineToolbar: true,
      },

      quote: {
        class: Quote,
        inlineToolbar: true,
        config: {
          quotePlaceholder: 'Enter a quote',
          captionPlaceholder: 'Quote\'s author',
        },
        shortcut: 'CMD+SHIFT+O'
      },

      warning: Warning,

      marker: {
        class:  Marker,
        shortcut: 'CMD+SHIFT+M'
      },

      code: {
        class:  CodeTool,
        shortcut: 'CMD+SHIFT+C'
      },

      delimiter: Delimiter,

      inlineCode: {
        class: InlineCode,
        shortcut: 'CMD+SHIFT+C'
      },

      linkTool: {
        class: LinkTool,
        config: {
          endpoint: '/fetchUrl', // Your backend endpoint for url data fetching
        },
      },

      embed: Embed,

      table: {
        class: Table,
        inlineToolbar: true,
        shortcut: 'CMD+ALT+T'
      },
    },

    data: data,

    onReady: function(){
      // saveButton.click();
    },
    onChange: function() {
      console.log('something changed');
    }
  });
  saveButton.addEventListener('click', function () {
    editor.save().then((savedData) => {
      var data = JSON.stringify(savedData);
      let parts = window.location.pathname.split( '/' );
      let url = '/api/v1/articles/' + parts[3];
      $.ajax({
          url: url,
          type: 'PUT',
          contentType: 'application/json; charset=utf-8',
          data: data,
          success: function (response) {
              $("#saved").delay(20).fadeIn(500);
              $("#saved").delay(2000).fadeOut(500);
          },
          error: function (xhr) {
              alert('Error: There was some error while posting. Please try again later.');
          }
      });
    });
  });

};
