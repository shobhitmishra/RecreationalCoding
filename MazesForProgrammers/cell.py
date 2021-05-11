from typing import Any, cast, Dict, Hashable, List, Optional
import warnings

# Define Links and CellList type
Links = Dict["Cell", bool]
CellList = List["Cell"]

class Cell:
    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    @property
    def links(self) -> CellList:
        return list(self._links.keys())

    # getter only property for neighbor.
    @property
    def neighbors(self) -> CellList:
        neighbors_list: CellList = []
        if self.north:
            neighbors_list.append(self.north)
        if self.south:
            neighbors_list.append(self.south)
        if self.east:
            neighbors_list.append(self.east)
        if self.west:
            neighbors_list.append(self.west)
        return neighbors_list

    def __init__(self, row: int, column: int) -> None:
        if row is None or row < 0:
            raise ValueError("Row must be a positive integer")
        if column is None or column < 0:
            raise ValueError("Column must be a positive integer")

        self._row: int = row
        self._column: int = column
        self._links: Dict[Cell, bool] = {}
        #self._data: Dict = {}
        self.north: Optional[Cell] = None
        self.south: Optional[Cell] = None
        self.east: Optional[Cell] = None
        self.west: Optional[Cell] = None

    def link(self, cell: "Cell", bidirectional: bool = True) -> "Cell":
        """
        Links current cell to specified one
        """
        if not is_cell(cell):
            raise ValueError("Link can only be made between two cells")

        self._links[cell] = True
        if bidirectional:
            cell.link(cell=self, bidirectional=False)
        return self

    def unlink(self, cell: "Cell", bidirectional: bool = True) -> "Cell":
        """
        Unlinks current cell from specified one
        """
        if cell is None:
            warnings.warn("Attempted to remove non-existant link", UserWarning)
        elif not is_cell(cell):
            raise ValueError("Link can only be removed between two cells")

        if self.linked_to(cell):
            del self._links[cell]
            if bidirectional:
                cell.unlink(cell=self, bidirectional=False)
        return self
    
    def is_cell(cell: Any) -> bool:
        return isinstance(cell, Cell)

    def linked_to(self, cell: Optional["Cell"]) -> bool:
        if is_cell(cell):
            return cell in self._links
        elif cell is None:
            return False
        else:
            raise ValueError("Attempted to check link with non-cell")