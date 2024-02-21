; Include statement

(include) @keyword
(filename) @string


; Document part

;(document_part "." @operator)
;(document_part_type) @namespace

; Let client do the title, use LS just to highlight environments in title
;(document_part_title) @variable


; Object
;(object ["." ":"] @operator)
;(object_type) @storage.type.struct


; Block

;  - Short Inner Environment

;(short_inner_environment ["." ":"] @operator)
;(short_inner_environment_type) @type
;(short_inner_environment_body) @parameter

;  - Verbose Inner Environment

;(verbose_inner_environment (_ "\"" @string))
;(verbose_inner_environment (_ ["." "@" "#"] @operator))
;(verbose_inner_environment_type) @method
;(verbose_inner_environment_at_end) @method
;(verbose_inner_environment_meta) @modifier

;  - Outer Environment

;(outer_environment_type) @variable.other
;(fragile_outer_environment ["!" ":"] @operator)
;(classic_outer_environment ["." ":"] @operator)

;  - Math

;(math_environment "$" @function)
;(math_environment_body ) @number
