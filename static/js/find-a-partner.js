YUI({
  comboBase: 'https://yui-s.yahooapis.com/combo?',
  combine: true
}).use('autocomplete-base', 'autocomplete-filters', 'node-event-simulate', function (Y) {

  // Create a custom PartnerFilter class that extends AutoCompleteBase.
  var PartnerFilter = Y.Base.create('partnerFilter', Y.Base, [Y.AutoCompleteBase], {
    initializer: function () {
      this._bindUIACBase();
      this._syncUIACBase();
    }
  }),

  // Create instance
  search = new PartnerFilter({
    inputNode: '.p-find-a-partner__search-input',
    minQueryLength: 0,
    queryDelay: 0,

    // Immediately-invoked function to gather data
    source: (function () {
      var results = [];

      Y.all('.p-find-a-partner__partner').each(function (node) {
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
    var numberOfPartners = Y.all('.p-find-a-partner__partner').size();
    var numberOfSearchMisses = Y.all('.not-search-match').size();
    var numberOfFilterMisses = Y.all('.not-filter-match').size();
    if (numberOfSearchMisses == numberOfPartners || numberOfFilterMisses == numberOfPartners) {
      return false;
    } else {
      return true;
    }
  }

  function updateNoResultsMessage(matchesExist) {
    if (matchesExist){
      Y.one('.p-find-a-partner__no-results').addClass('u-hide');
    } else {
      Y.one('.p-find-a-partner__no-results').removeClass('u-hide');
    }
  }

  function cloneItem(node, exact) {
      var container = Y.one('.p-find-a-partner__prioritised-results');
      clone = node.cloneNode(true);
      node.addClass('match-hide');
      if(exact) {
        container.prepend(clone);
      } else {
        container.append(clone);
      }
  }

  function prioritiseTitleMatches(search) {
    //clone any exact title matches and hide the original
    partners = Y.all('.p-find-a-partner__partner');

    partners.each(function(partner) {
      partnerTitle = partner.getAttribute('ID');
      if (partnerTitle == search) {
        cloneItem(partner, true);
      } else {
        if (partnerTitle.indexOf(search) != -1) {
          cloneItem(partner, false);
        }
      }
    });
  }

  // Subscribe to the "results" event
  search.on('results', function (e) {
    Y.one('.p-find-a-partner__partner-list').addClass('u-hide');
    Y.all('.p-find-a-partner__partner').addClass('not-search-match');
    Y.one('.p-find-a-partner__prioritised-results').empty();
    Y.Array.each(e.results, function (result) {
      result.raw.node.removeClass('not-search-match');
      result.raw.node.removeClass('match-hide');
    });
    prioritiseTitleMatches(e.query);
    updateNoResultsMessage(matchesExist());
  });

  //Adds a listener to checkboxes to filter results
  var checkboxes = Y.all('.p-find-a-partner__filter"');
  checkboxes.on('change', function (e) {
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
    partners = Y.all('.p-find-a-partner__partner');
    partners.each(function(node) {
      node.addClass('not-filter-match');
    });
    partners.each(function(node) {
      dataFilter = node.getAttribute('data-filter');
      for (var name in filters) {
        if (filters[name] == true && dataFilter.indexOf(name) != -1) {
          node.removeClass('not-filter-match');
        }
      }
    });

    if (filters.indexOf(true) == -1) {
      if (partners.size() == Y.all('.not-filter-match').size()) {
        partners.each(function(node){
          node.removeClass('not-filter-match');
        });
      }
    };
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
          returnParams[queryArray[0].toLowerCase()] = new Array;
        }
        if (queryArray.length == 1) {
          //query param is just a key
          returnParams[queryArray[0]] = "";
        } else {
          //query param is key/value
          var rawQueryParam = decodeURIComponent(queryArray[1]);
          var cleanQueryParam = rawQueryParam.replace("/", "").replace(/\W+/g, "-").toLowerCase(); //sanitise raw input
          returnParams[queryArray[0].toLowerCase()].push(cleanQueryParam);
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
    var searchbox = Y.one('.p-find-a-partner__search-input');
    var searchText = getParameterByName('search');
    if (searchbox != null && searchText != null) {
      searchbox.focus();
      searchbox.set('value', searchText);
    }
  }

  populateCheckboxes();
  populateTextbox();


  Y.all('.p-find-a-partner js-search-not-run').removeClass('js-search-not-run');
});
