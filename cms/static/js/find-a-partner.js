YUI().use('autocomplete-base', 'autocomplete-filters', 'node-event-simulate', function (Y) {
  // Create a custom PartnerFilter class that extends AutoCompleteBase.
  var PartnerFilter = Y.Base.create('partnerFilter', Y.Base, [Y.AutoCompleteBase], {
    initializer: function () {
      this._bindUIACBase();
      this._syncUIACBase();
    }
  }),

  // Create instance
  search = new PartnerFilter({
    inputNode: '#search',
    minQueryLength: 0,
    queryDelay: 0,

    // Immediately-invoked function to gather data
    source: (function () {
      var results = [];

      Y.all('#results > .partner').each(function (node) {
        results.push({
          node: node,
          searchText: node.getAttribute('data-searchText')
        });
      });

      return results;
    }()),

    resultTextLocator: 'searchText',

    // filter on part-words
    resultFilters: 'subWordMatch'
  });

  // Returns true if there are any matched results
  function matchesExist() {
    if (Y.all('#results > .partner').size() == (Y.all('#results > .notSearchMatch').size() + Y.all('#results > .notFilterMatch').size())){
      return false;
    } else {
      return true;
    }
  }

  function updateNoResultsMessage(matchesExist) {
    if (matchesExist){
      Y.one('#results .noResults').addClass('hide');
    } else {
      Y.one('#results .noResults').removeClass('hide');
    }
  }

  function prioritiseTitleMatches(search) {
    //clone any exact title matches and hide the original
    partners = Y.all('#results > .partner');
    match = partners.filter('#'+search);
    //clone
    if (match.item(0) !== null) {
      clone = match.item(0).cloneNode(true);
      match.addClass('matchHide');
      Y.one('.prioritisedResults').append(clone);
      Y.one('.prioritisedResults').removeClass('hidden');
    }
  }

  // Subscribe to the "results" event
  search.on('results', function (e) {
    Y.all('#results > .partner').addClass('notSearchMatch');
    Y.one('.prioritisedResults').empty();
    Y.one('.prioritisedResults').addClass('hidden');
    Y.Array.each(e.results, function (result) {
      result.raw.node.removeClass('notSearchMatch');
      result.raw.node.removeClass('matchHide');
    });

    prioritiseTitleMatches(e.query);

    updateNoResultsMessage(matchesExist());
  });

  //Adds a listener to checkboxes to filter results
  var checkboxes = Y.all('.search-panel input[type=checkbox]');
  checkboxes.on('change', function (e) { console.log('change detected');
    var checkbox = e.target;
    var checked = checkbox.get('checked');
    var attributeName = checkbox.get('id')
    updateFilter(attributeName, checked);
    updateNoResultsMessage(matchesExist());
  });

  var filters = [];
  //Adds the provided filter and filters the results accordingly
  function updateFilter(name, add) {
    filters[name] = add;
    partners = Y.all('.partner');
    partners.each(function(node) {
      node.addClass('notFilterMatch');
    });
    partners.each(function(node) {
      dataFilter = node.getAttribute('data-filter');
      for (var name in filters) {
        if (filters[name] == true && dataFilter.indexOf(name) != -1) {
          node.removeClass('notFilterMatch');
        }
      }
    });
    
    if (filters.indexOf(true) == -1) {
      if (partners.size() == Y.all('.notFilterMatch').size()) {
        partners.each(function(node){
          node.removeClass('notFilterMatch');
        });
      }
    } console.log(filters);
  }

  //Get specified query param
  function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"), results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
  }

  //check any checkboxes that match URL queries
  function populateCheckboxes() {
    //get URL query params
    var queryParams = (function(queryString) {
      if (queryString == "") return {};
      var returnParams = {};
      for (var i = 0; i < queryString.length; ++i) {
        var queryArray=queryString[i].split('=', 2);
        if ( Object.prototype.toString.call( returnParams[queryArray[0]] ) !== '[object Array]' ) {
          returnParams[queryArray[0]] = new Array;
        }
        if (queryArray.length == 1) {
          //returnParams[queryArray[0]] = "";
        } else {
          returnParams[queryArray[0]].push(decodeURIComponent(queryArray[1].replace(/\+/g, " ")));
        }
      }
      return returnParams;
    })(window.location.search.substr(1).split('&'));

    //check any appropriate checkboxes
    for (var key in queryParams) {
      for (var i = 0; i < queryParams[key].length; ++i) {
        var checkboxObject = Y.one('#' + key + '-' + queryParams[key][i]);
        if (checkboxObject != null) {
          checkboxObject.setAttribute('checked','checked');
          updateFilter(key + '-' + queryParams[key][i], true);
          Y.one('#'+key).addClass('open');
        }
      }
    }
  }

  //auto-fill text search
  function populateTextbox() {
    var searchbox = Y.one('#search');
    var searchText = getParameterByName('search');
    if (searchbox != null && searchText != null) {
      searchbox.focus();
      searchbox.set('value', searchText);
    }
  }

  populateCheckboxes();
  populateTextbox();
});