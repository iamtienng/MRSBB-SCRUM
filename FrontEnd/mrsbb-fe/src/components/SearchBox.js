import React from "react";

const SearchBox = (props) => {
  return (
    <div className="">
      <input
        className="form-controll"
        value={props.value}
        onChange={(event) => props.setSearch(event.target.value)}
        placeholder="Type to search.."
      ></input>
    </div>
  );
};

export default SearchBox;
