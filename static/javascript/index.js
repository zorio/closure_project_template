goog.provide('sample.index');
goog.require('goog.dom');
goog.require('goog.soy');
goog.require('sample.soy.index');

sample.index = function() {
  goog.dom.append(
      document.body,
      goog.soy.renderAsElement(sample.soy.index.drawIndex, {title: 'Index'}));
};

new sample.index();
