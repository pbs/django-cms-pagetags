function autocomplete(id, url) {

    function split(val) { return val.split(/,\s*/); }
    function extractLast(term) { return split(term).pop(); }

    el = $(document.getElementById(id));

    el
    .bind( "keydown", function( event ) {
        if (event.keyCode === $.ui.keyCode.TAB && $(this).data("autocomplete").menu.active) {
            event.preventDefault();
        }
    })
    .autocomplete({
        source: function(request, response) {
            $.getJSON(url, {q: extractLast(request.term)}, response);
        },

        search: function() {
            var term = extractLast(this.value);
            if (term.length < 2) {
                    return false;
            }
        },

        focus: function() { return false; },

        select: function(event, ui) {
                var terms = split(this.value);
                // remove the current input
                terms.pop();
                // add the selected item
                terms.push(ui.item.value);
                // add placeholder to get the comma-and-space at the end
                terms.push("");
                this.value = terms.join(", ");
                return false;
        }
    });

};
