(function () {
  Math.random = function() {
    return 0;
  };
})();
(function () {
  var orig_date = Date;
  var time_seed = 1542295966157;
  Date = function() {
    return orig_date(time_seed);
  };
  Date.__proto__ = orig_date;
  Date.prototype = orig_date.prototype;
  Date.prototype.constructor = Date;
  orig_date.now = function() {
    return new Date().getTime();
  };
})();
