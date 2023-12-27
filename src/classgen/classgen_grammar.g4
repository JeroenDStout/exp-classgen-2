grammar classgen_grammar;	
    
// ------------------------------
//      tokens
// ------------------------------

NEWLINE         : [\r\n]+    -> channel( HIDDEN );
WHITESPACE      : [ \n\t\r]+ -> channel( HIDDEN );

// brackets
TOKEN_CURL_LH   : '{'     ;
TOKEN_CURL_RH   : '}'     ;
TOKEN_SQUARE_LH : '['     ;
TOKEN_SQUARE_RH : ']'     ;
TOKEN_ROUND_LH  : '('     ;
TOKEN_ROUND_RH  : ')'     ;
TOKEN_ANG_LH    : '<'     ;
TOKEN_ANG_RH    : '>'     ;

// operators
TOKEN_ARROW_LW  : '<-'    ;
TOKEN_ARROW_RW  : '->'    ;
TOKEN_ARROW_SYM : '<->'   ;
TOKEN_IPLMAP_LW : ':<'    ;
TOKEN_IPLMAP_RW : ':>'    ;
TOKEN_PLUS      : '+'     ;
TOKEN_MINUS     : '-'     ;
TOKEN_DCOLON    : '::'    ;
TOKEN_DDOT      : '..'    ;

// useful keywords
KEYWORD_TAG      : 'tag'      ;
KEYWORD_AKA      : 'aka'      ;
KEYWORD_AS       : 'as'       ;
KEYWORD_WITH     : 'with'     ;
KEYWORD_IN       : 'in'       ;
KEYWORD_TO       : 'to'       ;
KEYWORD_FOR      : 'for'      ;
KEYWORD_TEMPLATE : 'template' ;

// intrinsic
KEYWORD_BOOL    : 'bool'  ;
TOKEN_TRUE      : 'true'  ;
TOKEN_FALSE     : 'false' ;

// types
KEYWORD_REFL    : 'refl'  ;
KEYWORD_POD     : 'pod'   ;
KEYWORD_ENUM    : 'enum'  ;
KEYWORD_PROC    : 'proc'  ;

IDENTIFIER_LIKE_INTRINSIC_INT
    : ('i' | 'u') FRAG_DEC_NAT_NUMBER FRAG_NONDIGIT (FRAG_NONDIGIT | FRAG_DIGIT)*
    ;
    
INTRINSIC_SINT
    : 'i' FRAG_DEC_NAT_NUMBER
    ;
    
INTRINSIC_UINT
    : 'u' FRAG_DEC_NAT_NUMBER
    ;
    
IDENTIFIER
    : FRAG_NONDIGIT (FRAG_NONDIGIT | FRAG_DIGIT)*
    | IDENTIFIER_LIKE_INTRINSIC_INT
    ;
    
FRAG_DEC_NAT_NUMBER
    : FRAG_DIGIT+
    ;

FRAG_NONDIGIT        : [a-zA-Z_] ;
FRAG_DIGIT           : [0-9]     ;

// ------------------------------
//    prog
// ------------------------------

prog
    : translation_unit EOF
    ;

translation_unit
    : translation_unit_object*
    ;

translation_unit_object
    : definition_object
    ;
    
// ------------------------------
//      intrinsics
// ------------------------------

intrinsic
    : intrinsic_boolean
    | intrinsic_unsigned_integer
    | intrinsic_signed_integer
    ;
    
intrinsic_boolean
    : KEYWORD_BOOL
    ;

intrinsic_unsigned_integer
    : INTRINSIC_UINT
    ;
    
intrinsic_signed_integer
    : INTRINSIC_SINT
    ;
    
// ------------------------------
//      constants
// ------------------------------

constant
    : constant_boolean
    | constant_integer
    ;
    
constant_boolean
    : (constant_boolean_true | constant_boolean_false)
    ;
    
constant_boolean_true
    : TOKEN_TRUE
    ;
    
constant_boolean_false
    : TOKEN_FALSE
    ;
    
constant_integer
    : FRAG_DEC_NAT_NUMBER
    ;
    
// ------------------------------
//      identifiers
// ------------------------------
    
identifier_name
    : identifier_namespace_pre? IDENTIFIER
    ;
    
identifier_pure
    : identifier_name identifier_postfix?
    ;
    
identifier_ex
    : identifier_pure
    | identifier_with_alias
    ;
    
identifier_with_alias
    : identifier_name identifier_postfix? KEYWORD_AKA identifier_alias_list
    ;
    
identifier_alias_list
    : identifier_name (',' identifier_name)*
    ;
    
identifier_postfix
    : identifier_namespace_post
    ;
    
identifier_namespace_pre
    : identifier_namespace_list TOKEN_DCOLON
    ;
    
identifier_namespace_post
    : KEYWORD_IN identifier_namespace_list
    ;
    
identifier_namespace_list
    : identifier_namespace_list_element (TOKEN_DCOLON identifier_namespace_list_element)*
    ;
    
identifier_namespace_list_element
    : IDENTIFIER
    | TOKEN_DDOT
    ;

// ------------------------------
//    objects declarations
// ------------------------------

object_type
  : KEYWORD_REFL | KEYWORD_ENUM | KEYWORD_POD | KEYWORD_PROC
  ;

definition_object
  : object_type identifier_ex definition_object_body
  ;

definition_object_body
  : definition_object_body_curl
  | definition_object_body_square
  ;

definition_object_body_curl
  : TOKEN_CURL_LH definition_object_element* TOKEN_CURL_RH
  ;

definition_object_body_square
  : TOKEN_SQUARE_LH definition_object_element* TOKEN_SQUARE_RH
  ;

definition_object_element
  : definition_object_abracket_list
  | definition_object_sbracket_list
  | definition_object_with_statement
  | definition_object_identifier
  | definition_object_implied_map
  | definition_object
  ;

definition_object_meta
  : definition_meta_tag_statement
  | definition_meta_template_statement
  | definition_meta_for_statement
  | definition_meta_refl_statement
  ;

definition_object_identifier
  : identifier_ex definition_object_identifier_postlist?
  ;

definition_object_identifier_postlist
  : definition_object_identifier_postlist_elem+
  ;

definition_object_identifier_postlist_elem
  : TOKEN_ROUND_LH definition_object_identifier_postlist TOKEN_ROUND_RH
  | definition_object_implied_map
  ;
  
definition_object_sbracket_list
  : TOKEN_SQUARE_LH definition_object_element* TOKEN_SQUARE_RH
  ;
  
definition_object_abracket_list
  : TOKEN_ANG_LH definition_object_meta* TOKEN_ANG_RH
  ;

definition_object_with_statement
  : KEYWORD_WITH identifier_ex
  ;

definition_object_implied_map
  : identifier_ex TOKEN_IPLMAP_RW definition_object_implied_map_to_value definition_object_implied_map_default?
  ;

definition_object_implied_map_to_value
  : mapping_value_constant
  | identifier_pure
  | intrinsic
  | definition_object
  ;

definition_object_implied_map_default
  : TOKEN_CURL_LH mapping_value TOKEN_CURL_RH
  ;

definition_meta_tag_statement
  : KEYWORD_TAG IDENTIFIER
  ;

definition_meta_template_statement
  : KEYWORD_TEMPLATE identifier_pure
  ;

definition_meta_for_statement
  : KEYWORD_FOR object_type
  ;

definition_meta_refl_statement
  : KEYWORD_REFL identifier_pure
  ;

mapping_value
  : mapping_value_constant
  | identifier_pure
  ;

mapping_value_constant
  : constant
  ;