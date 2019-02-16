# DiceDistributions

Evaluate discrete probability distributions of RPG dice math

## Usage

```
python main.py 'dice-math'
python main.py 'options:dice-math'
```
where dice-math is a standard mathematical infix expression.

```
> python main.py '2d6 + 4'
Expected value: 11.000
6:   2.778%  ██████████████
7:   5.556%  ███████████████████████████
8:   8.333%  ████████████████████████████████████████
9:  11.111%  ██████████████████████████████████████████████████████
10: 13.889%  ████████████████████████████████████████████████████████████████████
11: 16.667%  █████████████████████████████████████████████████████████████████████████████████
12: 13.889%  ████████████████████████████████████████████████████████████████████
13: 11.111%  ██████████████████████████████████████████████████████
14:  8.333%  ████████████████████████████████████████
15:  5.556%  ███████████████████████████
16:  2.778%  ██████████████

> python main.py "d20>=3d6"
Expected value:  0.525
False: 47.500%  ███████████████████████████████████████████████████████████████████████
True:  52.500%  ██████████████████████████████████████████████████████████████████████████████
```

### Supported dice and primitives

- Regular numbered dice ```[R]dN```: N-sided die repeated R times. e.g. 3d6, d20
- Fate dice ```[R]F```: Fate die (-1,-1,0,0,1,1) thrown R times. e.g. F, 3F
- Constant integers

### Supported math operators

- ```+```: add
- ```-```: subtract
- ```*```: multiply
- ```=```: equal to
- ```<```: less than
- ```>```: more than
- ```<=```: less than or equal to
- ```>=```: more than or equal to

### Options

Running options change the way results are displayed.

- ```S```, runs a statistical simulation instead of giving analytic results. Give interrupt signal (Ctrl-C) to stop.
- ```O```, displays odds instead of a graph result
- ```C```, displays the result in cumulative form

```
> python main.py 'O:2d6'
Expected value:  7.000
2:   2.778%  1:35
3:   5.556%  1:17
4:   8.333%  1:11
5:  11.111%  1:8
6:  13.889%  5:31
7:  16.667%  1:5
8:  13.889%  5:31
9:  11.111%  1:8
10:  8.333%  1:11
11:  5.556%  1:17
12:  2.778%  1:35
```

## License

MIT Licence (c) Lauri Tervonen 2019. Check LICENSE-file for details.
