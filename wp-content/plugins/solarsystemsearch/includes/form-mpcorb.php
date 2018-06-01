<form id="ssswp-form">
<input type="hidden" name="searchtool" value="SQL">
<input type="hidden" name="TaskName" value="SolarSystemSearch">
<input type="hidden" name="syntax" value="Syntax">
<input type="hidden" name="ReturnHtml" value="true">
<input type="hidden" name="format" value="html">
<input type="hidden" name="TableName" value="">
<input type="hidden" name="ssswp-query" value="">
<div class="form-group">
Select the first <select name="_num" id="ssswp-num">
  <option value="10" selected>10</option>
  <option value="50">50</option>
  <option value="100">100</option>
  <option value="500">500</option>
  <option value="100">1000</option>
  <option value="1000">10000</option>
  <option value="3000">30000</option>
</select> asteroids.
</div>
<div class="form-group">
Return asteroid coordinates as <select name="_coords" id="ssswp-coord">
  <option value="radec" selected>RA and Dec</option>
  <option value="ecli" data-ssswp-fields="nodeAscendingLongitude,inclination" >Ecliptic longitude and latitude</option>
</select> .
</div>
<textarea id="ssswp-query" name="cmd" class="ssswp-query" rows=4 cols=80 ssswp-data-query="select top _num name, _coords from mpcorb" disabled >select top 10 name, ra, dec from mpcorb</textarea><br>
<button id="ssswp-submit" name="ssswp-submit" class="ssswp-submit btn btn-success">Submit</button>
</form>
