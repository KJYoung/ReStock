// Generated by ReScript, PLEASE EDIT WITH CARE

import * as Chai from "chai";
import * as React from "react";
import * as App$Restock from "../App.bs.js";
import * as React$1 from "@testing-library/react";

it("renders learn react link", (function () {
        React$1.render(React.createElement(App$Restock.make, {}));
        var actual = React$1.getNodeText(React$1.screen.getByText("Learn React"));
        Chai.assert.equal(actual, "Learn React");
      }));

export {
  
}
/*  Not a pure module */
