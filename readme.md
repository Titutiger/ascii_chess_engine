# ASCII-Chess Engine
###### ~ Python
___
~ Aarin and Ojas

###### 12/11/2025
___
### Aarin:
- [x] Design overall project structure and modules
- [ ] Implement commandline argument parser (DEPRECATED)
- [ ] Implement AI engine (stockfish) for `pvm`
- [x] Implement chess notation as user input
- [x] Implement special moves like `en passant, castling, pawn promotion, etc...`
 

___
### Ojas:
- [x] Create ASCII art for chess pieces procedurally
- [x] Develop terminal board refresh dynamically after moves
- [ ] Write game loop for `pvp`
- [x] Integrate basic move rules and legality checks
- [x] Handle game conditions like `checkmate`, `stalemate` and `draw`

___

### Project details and structure:
`python environment: 3.12`

File structure:
```
ascii_chess_engine
- /.venv
  ...
- /src
  - /utils
    - function.py files
  - main.py
- /docs
  - readme.md
```

Variable structure:
```python
# variable notation must be in snake case!
variable_name: data_type = value
```

Function structure:
```python
def function(parameter: data_type) -> return data_type:
    """
    ...
    
    Parameters:
    -----------
    ...
    
    Returns:
    --------
    ...
    
    Raises:
    -------
    ...
    
    Examples:
    ---------
    ...
    """
    ...
```

Grid (array):
```python
import numpy as np
array: np.ndarray = np.array(
    [... , ... , ...]
)
matrix: np.ndarray = np.array(
    [
        [... , ...],
        [... , ...],
    ]
)
```