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

let url = 'http://localhost:4006/getjson/' + findGetParameter("id") ;

async function fetchData() {
  return fetch(url)
    .then(data => {return data.json() })
    .then(res => { createEditor(res) })
}

fetchData()

function createEditor(data){
  var editor = new EditorJS({
    /**
     * Wrapper of Editor
     */
    holder: 'editorjs',
    placeholder: '... schreibe los ...',
    /**
     * Tools list
     */
    tools: {
      /**
       * Each Tool is a Plugin. Pass them via 'class' option with necessary settings {@link docs/tools.md}
       */
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
      image: SimpleImage,

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
      $.ajax({
          url: '/postjson/{{ id }}',
          type: 'POST',
          contentType: 'application/json; charset=utf-8',
          data: data,
          success: function (response) {
              $("#saved").delay(20).fadeIn(500);
              // $("#saved").css("visibility", "visible");
              $("#saved").delay(2000).fadeOut(500);
          },
          error: function (xhr) {
              alert('Error: There was some error while posting. Please try again later.');
          }
      });
    });
  });

};
