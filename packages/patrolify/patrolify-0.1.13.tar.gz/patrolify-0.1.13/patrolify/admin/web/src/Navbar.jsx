import {
  Button,
  Classes,
  Navbar,
  NavbarDivider,
  NavbarGroup,
  NavbarHeading,
  Tag,
} from "@blueprintjs/core";
import { Link } from "react-router-dom";
import { version } from "./version";

export default function AppNavbar() {
  return (
    <Navbar>
      <NavbarGroup>
        <NavbarHeading>Reporter
          <Tag intent="primary" style={{ marginLeft: "3px" }} minimal>v{version}</Tag>
        </NavbarHeading>
        <NavbarDivider />
        <Link to="/">
          <Button className={Classes.MINIMAL} icon="home" text="Home" />
        </Link>
        <Link to="/files?path=checkers">
          <Button className={Classes.MINIMAL} icon="code" text="Code Explorer" />
        </Link>
        <Link to="/files?path=results">
          <Button className={Classes.MINIMAL} icon="box" text="History" />
        </Link>
      </NavbarGroup>
      <NavbarGroup align="right">
        <Link to="https://github.com/laixintao/patrolify">
          <Button className={Classes.MINIMAL} icon="git-repo" text="Source Code" />
        </Link>
      </NavbarGroup>

    </Navbar>
  );
}
