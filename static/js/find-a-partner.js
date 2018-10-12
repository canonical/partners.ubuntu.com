(function() {
  function init() {
    var inputNode = document.querySelector(".p-find-a-partner__search-input");
    var minQueryLength = 0;
    var queryDelay = 0;

    var results = [];

    inputNode.addEventListener("keydown", search);

    var partners = document.querySelectorAll(".p-find-a-partner__partner");
    partners.forEach(function(node) {
      results.push({
        node: node,
        searchText: node.getAttribute("data-searchText")
      });
    });

    var resultTextLocator = "searchText";

    // filter on part-words
    var resultFilters = "subWordMatch";
  }

  // Returns true if there are any matched results
  function matchesExist() {
    var numberOfPartners = document.querySelectorAll(
      ".p-find-a-partner__partner"
    ).length;
    var numberOfSearchMisses = document.querySelectorAll(".not-search-match")
      .length;
    var numberOfFilterMisses = document.querySelectorAll(".not-filter-match")
      .length;
    if (
      numberOfSearchMisses == numberOfPartners ||
      numberOfFilterMisses == numberOfPartners
    ) {
      return false;
    } else {
      return true;
    }
  }

  function updateNoResultsMessage(matchesExist) {
    if (matchesExist) {
      var partnerGood = document.querySelector(".p-find-a-partner__no-results");
      partnerGood.classList.add("u-hide");
    } else {
      var partnerBad = document.querySelector(".p-find-a-partner__no-results");
      partnerBad.classList.remove("u-hide");
    }
  }

  function cloneItem(node, exact) {
    var container = document.querySelector(
      ".p-find-a-partner__prioritised-results"
    );
    clone = node.cloneNode(true);
    node.classList.add("match-hide");
    if (exact) {
      container.prepend(clone);
    } else {
      container.append(clone);
    }
  }

  function prioritiseTitleMatches(search) {
    //clone any exact title matches and hide the original
    var partners = document.querySelectorAll(".p-find-a-partner__partner");

    partners.forEach(function(partner) {
      partnerTitle = partner.getAttribute("ID");
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
  function search(e) {
    console.log("start", e.target.value);
    var partnerList = document.querySelector(".p-find-a-partner__partner-list");
    partnerList.classList.add("u-hide");
    var partners = document.querySelectorAll(".p-find-a-partner__partner");
    partners.forEach(function(partner) {
      partner.classList.add("u-hide");
    });
    var priorityResults = document.querySelector(
      ".p-find-a-partner__prioritised-results"
    );
    var results = document.querySelectorAll(".p-find-a-partner__partner");
    partners.forEach(function(partner) {
      partner.classList.remove("u-hide");
    });
    prioritiseTitleMatches(e.query);
    updateNoResultsMessage(matchesExist());
  }

  //Adds a listener to checkboxes to filter results
  var checkboxes = document.querySelectorAll(".p-find-a-partner__filter");
  checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener("change", function(e) {
      console.log("change");
      var checkbox = e.target;
      var checked = checkbox.checked;
      var attributeName = checkbox.id;
      updateFilter(attributeName, checked);
      updateNoResultsMessage(matchesExist());
    });
  });

  var filters = [];
  //Adds the provided filter and filters the results accordingly
  function updateFilter(name, add) {
    filters[name] = add;
    partners = document.querySelectorAll(".p-find-a-partner__partner");
    partners.forEach(function(node) {
      node.classList.add("u-hide");
    });
    partners.forEach(function(node) {
      dataFilter = node.getAttribute("data-filter");
      for (var name in filters) {
        if (filters[name] == true && dataFilter.indexOf(name) != -1) {
          node.classList.remove("u-hide");
        }
      }
    });

    if (filters.indexOf(true) == -1) {
      if (
        partners.length ==
        document.querySelectorAll(".p-find-a-partner__partner.u-hide").length
      ) {
        partners.forEach(function(node) {
          node.classList.remove("u-hide");
        });
      }
    }
  }

  //Get specified query param
  function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
      results = regex.exec(location.search);
    return results == null
      ? ""
      : decodeURIComponent(results[1].replace(/\+/g, " "));
  }

  //check any checkboxes that match URL queries
  function populateCheckboxes() {
    //get URL query params
    var queryParams = (function(queryString) {
      if (queryString == "") return {};
      var returnParams = {};
      for (var i = 0; i < queryString.length; ++i) {
        var queryArray = queryString[i].split("=", 2);
        if (
          Object.prototype.toString.call(returnParams[queryArray[0]]) !==
          "[object Array]"
        ) {
          returnParams[queryArray[0].toLowerCase()] = new Array();
        }
        if (queryArray.length == 1) {
          //query param is just a key
          returnParams[queryArray[0]] = "";
        } else {
          //query param is key/value
          var rawQueryParam = decodeURIComponent(queryArray[1]);
          var cleanQueryParam = rawQueryParam
            .replace("/", "")
            .replace(/\W+/g, "-")
            .toLowerCase(); //sanitise raw input
          returnParams[queryArray[0].toLowerCase()].push(cleanQueryParam);
        }
      }
      return returnParams;
    })(window.location.search.substr(1).split("&"));

    //check any appropriate checkboxes
    for (var key in queryParams) {
      for (var i = 0; i < queryParams[key].length; ++i) {
        var checkboxObject = document.querySelector(
          "#" + key + "-" + queryParams[key][i]
        );
        if (checkboxObject != null) {
          checkboxObject.setAttribute("checked", "checked");
          updateFilter(key + "-" + queryParams[key][i], true);
          document.querySelector("#" + key).classList.add("open");
        }
      }
    }
  }

  //auto-fill text search
  function populateTextbox() {
    var searchbox = document.querySelector(".p-find-a-partner__search-input");
    var searchText = getParameterByName("search");
    if (searchbox != null && searchText != null) {
      searchbox.focus();
      searchbox.value = searchText;
    }
  }

  populateCheckboxes();
  populateTextbox();
  init();

  var removeSearch = document.querySelectorAll(
    ".p-find-a-partner js-search-not-run"
  );
  removeSearch.forEach(function(removed) {
    removed.classList.remove("js-search-not-run");
  });
})();
