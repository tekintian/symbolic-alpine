from __future__ import absolute_import
import os
import sys
from cffi import FFI

ffi = FFI()

ffi.cdef("""
enum SymbolicErrorCode {
  SYMBOLIC_ERROR_CODE_NO_ERROR = 0,
  SYMBOLIC_ERROR_CODE_PANIC = 1,
  SYMBOLIC_ERROR_CODE_UNKNOWN = 2,
  SYMBOLIC_ERROR_CODE_IO_ERROR = 101,
  SYMBOLIC_ERROR_CODE_UNKNOWN_ARCH_ERROR = 1001,
  SYMBOLIC_ERROR_CODE_UNKNOWN_LANGUAGE_ERROR = 1002,
  SYMBOLIC_ERROR_CODE_PARSE_DEBUG_ID_ERROR = 1003,
  SYMBOLIC_ERROR_CODE_UNKNOWN_OBJECT_KIND_ERROR = 2001,
  SYMBOLIC_ERROR_CODE_UNKNOWN_FILE_FORMAT_ERROR = 2002,
  SYMBOLIC_ERROR_CODE_OBJECT_ERROR_UNKNOWN = 2100,
  SYMBOLIC_ERROR_CODE_OBJECT_ERROR_UNSUPPORTED_OBJECT = 2101,
  SYMBOLIC_ERROR_CODE_OBJECT_ERROR_BAD_BREAKPAD_OBJECT = 2102,
  SYMBOLIC_ERROR_CODE_OBJECT_ERROR_BAD_ELF_OBJECT = 2103,
  SYMBOLIC_ERROR_CODE_OBJECT_ERROR_BAD_MACH_O_OBJECT = 2104,
  SYMBOLIC_ERROR_CODE_OBJECT_ERROR_BAD_PDB_OBJECT = 2105,
  SYMBOLIC_ERROR_CODE_OBJECT_ERROR_BAD_PE_OBJECT = 2106,
  SYMBOLIC_ERROR_CODE_OBJECT_ERROR_BAD_SOURCE_BUNDLE = 2107,
  SYMBOLIC_ERROR_CODE_OBJECT_ERROR_BAD_WASM_OBJECT = 2108,
  SYMBOLIC_ERROR_CODE_DWARF_ERROR_UNKNOWN = 2200,
  SYMBOLIC_ERROR_CODE_DWARF_ERROR_INVALID_UNIT_REF = 2201,
  SYMBOLIC_ERROR_CODE_DWARF_ERROR_INVALID_FILE_REF = 2202,
  SYMBOLIC_ERROR_CODE_DWARF_ERROR_UNEXPECTED_INLINE = 2203,
  SYMBOLIC_ERROR_CODE_DWARF_ERROR_INVERTED_FUNCTION_RANGE = 2204,
  SYMBOLIC_ERROR_CODE_DWARF_ERROR_CORRUPTED_DATA = 2205,
  SYMBOLIC_ERROR_CODE_CFI_ERROR_UNKNOWN = 3000,
  SYMBOLIC_ERROR_CODE_CFI_ERROR_MISSING_DEBUG_INFO = 3001,
  SYMBOLIC_ERROR_CODE_CFI_ERROR_UNSUPPORTED_DEBUG_FORMAT = 3002,
  SYMBOLIC_ERROR_CODE_CFI_ERROR_BAD_DEBUG_INFO = 3003,
  SYMBOLIC_ERROR_CODE_CFI_ERROR_UNSUPPORTED_ARCH = 3004,
  SYMBOLIC_ERROR_CODE_CFI_ERROR_WRITE_ERROR = 3005,
  SYMBOLIC_ERROR_CODE_CFI_ERROR_BAD_FILE_MAGIC = 3006,
  SYMBOLIC_ERROR_CODE_CFI_ERROR_INVALID_ADDRESS = 3007,
  SYMBOLIC_ERROR_CODE_PROCESS_MINIDUMP_ERROR_MINIDUMP_NOT_FOUND = 4001,
  SYMBOLIC_ERROR_CODE_PROCESS_MINIDUMP_ERROR_NO_MINIDUMP_HEADER = 4002,
  SYMBOLIC_ERROR_CODE_PROCESS_MINIDUMP_ERROR_NO_THREAD_LIST = 4003,
  SYMBOLIC_ERROR_CODE_PROCESS_MINIDUMP_ERROR_INVALID_THREAD_INDEX = 4004,
  SYMBOLIC_ERROR_CODE_PROCESS_MINIDUMP_ERROR_INVALID_THREAD_ID = 4005,
  SYMBOLIC_ERROR_CODE_PROCESS_MINIDUMP_ERROR_DUPLICATE_REQUESTING_THREADS = 4006,
  SYMBOLIC_ERROR_CODE_PROCESS_MINIDUMP_ERROR_SYMBOL_SUPPLIER_INTERRUPTED = 4007,
  SYMBOLIC_ERROR_CODE_PARSE_SOURCE_MAP_ERROR = 5001,
  SYMBOLIC_ERROR_CODE_SYM_CACHE_ERROR_UNKNOWN = 6000,
  SYMBOLIC_ERROR_CODE_SYM_CACHE_ERROR_BAD_FILE_MAGIC = 6001,
  SYMBOLIC_ERROR_CODE_SYM_CACHE_ERROR_BAD_FILE_HEADER = 6002,
  SYMBOLIC_ERROR_CODE_SYM_CACHE_ERROR_BAD_SEGMENT = 6003,
  SYMBOLIC_ERROR_CODE_SYM_CACHE_ERROR_BAD_CACHE_FILE = 6004,
  SYMBOLIC_ERROR_CODE_SYM_CACHE_ERROR_UNSUPPORTED_VERSION = 6005,
  SYMBOLIC_ERROR_CODE_SYM_CACHE_ERROR_BAD_DEBUG_FILE = 6006,
  SYMBOLIC_ERROR_CODE_SYM_CACHE_ERROR_MISSING_DEBUG_SECTION = 6007,
  SYMBOLIC_ERROR_CODE_SYM_CACHE_ERROR_MISSING_DEBUG_INFO = 6008,
  SYMBOLIC_ERROR_CODE_SYM_CACHE_ERROR_UNSUPPORTED_DEBUG_KIND = 6009,
  SYMBOLIC_ERROR_CODE_SYM_CACHE_ERROR_VALUE_TOO_LARGE = 6010,
  SYMBOLIC_ERROR_CODE_SYM_CACHE_ERROR_WRITE_FAILED = 6011,
  SYMBOLIC_ERROR_CODE_SYM_CACHE_ERROR_TOO_MANY_VALUES = 6012,
  SYMBOLIC_ERROR_CODE_UNREAL4_ERROR_UNKNOWN = 7001,
  SYMBOLIC_ERROR_CODE_UNREAL4_ERROR_EMPTY = 7002,
  SYMBOLIC_ERROR_CODE_UNREAL4_ERROR_BAD_COMPRESSION = 7004,
  SYMBOLIC_ERROR_CODE_UNREAL4_ERROR_INVALID_XML = 7005,
  SYMBOLIC_ERROR_CODE_UNREAL4_ERROR_INVALID_LOG_ENTRY = 7006,
  SYMBOLIC_ERROR_CODE_UNREAL4_ERROR_BAD_DATA = 7007,
  SYMBOLIC_ERROR_CODE_UNREAL4_ERROR_TRAILING_DATA = 7008,
  SYMBOLIC_ERROR_CODE_APPLE_CRASH_REPORT_PARSE_ERROR_IO = 8001,
  SYMBOLIC_ERROR_CODE_APPLE_CRASH_REPORT_PARSE_ERROR_INVALID_INCIDENT_IDENTIFIER = 8002,
  SYMBOLIC_ERROR_CODE_APPLE_CRASH_REPORT_PARSE_ERROR_INVALID_REPORT_VERSION = 8003,
  SYMBOLIC_ERROR_CODE_APPLE_CRASH_REPORT_PARSE_ERROR_INVALID_TIMESTAMP = 8004,
  SYMBOLIC_ERROR_CODE_APPLE_CRASH_REPORT_PARSE_ERROR_INVALID_IMAGE_IDENTIFIER = 8005
};

typedef struct SymbolicArchive SymbolicArchive;
typedef struct SymbolicCfiCache SymbolicCfiCache;
typedef struct SymbolicFrameInfoMap SymbolicFrameInfoMap;
typedef struct SymbolicObject SymbolicObject;
typedef struct SymbolicProguardMapper SymbolicProguardMapper;
typedef struct SymbolicSourceMapView SymbolicSourceMapView;
typedef struct SymbolicSourceView SymbolicSourceView;
typedef struct SymbolicSymCache SymbolicSymCache;
typedef struct SymbolicUnreal4Crash SymbolicUnreal4Crash;
typedef struct SymbolicUnreal4File SymbolicUnreal4File;

typedef struct {
    char *data;
    uintptr_t len;
    int owned;
} SymbolicStr;

typedef struct {
    uint64_t addr;
    const SymbolicStr *arch;
    int crashing_frame;
    uint32_t signal;
    uint64_t ip_reg;
} SymbolicInstructionInfo;

typedef struct {
    uint64_t sym_addr;
    uint64_t line_addr;
    uint64_t instr_addr;
    uint32_t line;
    SymbolicStr lang;
    SymbolicStr symbol;
    SymbolicStr filename;
    SymbolicStr base_dir;
    SymbolicStr comp_dir;
} SymbolicLineInfo;

typedef struct {
    SymbolicLineInfo *items;
    uintptr_t len;
} SymbolicLookupResult;

typedef struct {
    int symtab;
    int debug;
    int unwind;
    int sources;
} SymbolicObjectFeatures;

typedef struct {
    SymbolicStr os_name;
    SymbolicStr os_version;
    SymbolicStr os_build;
    SymbolicStr cpu_family;
    SymbolicStr cpu_info;
    uint32_t cpu_count;
} SymbolicSystemInfo;

typedef struct {
    SymbolicStr code_id;
    SymbolicStr code_file;
    SymbolicStr debug_id;
    SymbolicStr debug_file;
    uint64_t addr;
    uint64_t size;
} SymbolicCodeModule;

typedef struct {
    SymbolicStr name;
    SymbolicStr value;
} SymbolicRegVal;

typedef struct {
    uint64_t return_address;
    uint64_t instruction;
    uint32_t trust;
    SymbolicCodeModule module;
    SymbolicRegVal *registers;
    uintptr_t register_count;
} SymbolicStackFrame;

typedef struct {
    uint32_t thread_id;
    SymbolicStackFrame *frames;
    uintptr_t frame_count;
} SymbolicCallStack;

typedef struct {
    int32_t requesting_thread;
    uint64_t timestamp;
    int crashed;
    uint64_t crash_address;
    SymbolicStr crash_reason;
    SymbolicStr assertion;
    SymbolicSystemInfo system_info;
    SymbolicCallStack *threads;
    uintptr_t thread_count;
    SymbolicCodeModule *modules;
    uintptr_t module_count;
} SymbolicProcessState;

typedef struct {
    uint8_t data[16];
} SymbolicUuid;

typedef struct {
    SymbolicStr class_name;
    SymbolicStr method;
    SymbolicStr file;
    uintptr_t line;
} SymbolicJavaStackFrame;

typedef struct {
    SymbolicJavaStackFrame *frames;
    uintptr_t len;
} SymbolicProguardRemapResult;

typedef struct {
    uint32_t src_line;
    uint32_t src_col;
    uint32_t dst_line;
    uint32_t dst_col;
    uint32_t src_id;
    SymbolicStr name;
    SymbolicStr src;
    SymbolicStr function_name;
} SymbolicTokenMatch;

SymbolicStr symbolic_arch_ip_reg_name(const SymbolicStr *arch);
int symbolic_arch_is_known(const SymbolicStr *arch);
void symbolic_archive_free(SymbolicArchive *archive);
SymbolicArchive *symbolic_archive_from_bytes(const uint8_t *bytes, uintptr_t len);
SymbolicObject *symbolic_archive_get_object(const SymbolicArchive *archive, uintptr_t index);
uintptr_t symbolic_archive_object_count(const SymbolicArchive *archive);
SymbolicArchive *symbolic_archive_open(const char *path);
void symbolic_cficache_free(SymbolicCfiCache *cache);
SymbolicCfiCache *symbolic_cficache_from_object(const SymbolicObject *object);
const uint8_t *symbolic_cficache_get_bytes(const SymbolicCfiCache *cache);
uintptr_t symbolic_cficache_get_size(const SymbolicCfiCache *cache);
uint32_t symbolic_cficache_get_version(const SymbolicCfiCache *cache);
uint32_t symbolic_cficache_latest_version(void);
SymbolicCfiCache *symbolic_cficache_open(const char *path);
SymbolicStr symbolic_demangle(const SymbolicStr *ident, const SymbolicStr *lang);
SymbolicStr symbolic_demangle_no_args(const SymbolicStr *ident, const SymbolicStr *lang);
void symbolic_err_clear(void);
SymbolicStr symbolic_err_get_backtrace(void);
uint32_t symbolic_err_get_last_code(void);
SymbolicStr symbolic_err_get_last_message(void);
uint64_t symbolic_find_best_instruction(const SymbolicInstructionInfo *ii);
void symbolic_frame_info_map_add(SymbolicFrameInfoMap *frame_info_map, const SymbolicStr *debug_id, SymbolicCfiCache *cfi_cache);
void symbolic_frame_info_map_free(SymbolicFrameInfoMap *frame_info_map);
SymbolicFrameInfoMap *symbolic_frame_info_map_new(void);
SymbolicStr symbolic_id_from_breakpad(const SymbolicStr *breakpad_id);
void symbolic_init(void);
void symbolic_lookup_result_free(SymbolicLookupResult *lookup_result);
SymbolicStr symbolic_normalize_arch(const SymbolicStr *arch);
SymbolicStr symbolic_normalize_code_id(const SymbolicStr *code_id);
SymbolicStr symbolic_normalize_debug_id(const SymbolicStr *debug_id);
void symbolic_object_free(SymbolicObject *object);
SymbolicStr symbolic_object_get_arch(const SymbolicObject *object);
SymbolicStr symbolic_object_get_code_id(const SymbolicObject *object);
SymbolicStr symbolic_object_get_debug_id(const SymbolicObject *object);
SymbolicObjectFeatures symbolic_object_get_features(const SymbolicObject *object);
SymbolicStr symbolic_object_get_file_format(const SymbolicObject *object);
SymbolicStr symbolic_object_get_kind(const SymbolicObject *object);
SymbolicProcessState *symbolic_process_minidump(const char *path, const SymbolicFrameInfoMap *frame_info_map);
SymbolicProcessState *symbolic_process_minidump_buffer(const char *buffer, uintptr_t length, const SymbolicFrameInfoMap *frame_info_map);
void symbolic_process_state_free(SymbolicProcessState *process_state);
void symbolic_proguardmapper_free(SymbolicProguardMapper *mapper);
SymbolicUuid symbolic_proguardmapper_get_uuid(SymbolicProguardMapper *mapper);
int symbolic_proguardmapper_has_line_info(const SymbolicProguardMapper *mapper);
SymbolicProguardMapper *symbolic_proguardmapper_open(const char *path);
SymbolicStr symbolic_proguardmapper_remap_class(const SymbolicProguardMapper *mapper, const SymbolicStr *class_);
SymbolicProguardRemapResult symbolic_proguardmapper_remap_frame(const SymbolicProguardMapper *mapper, const SymbolicStr *class_, const SymbolicStr *method, uintptr_t line);
void symbolic_proguardmapper_result_free(SymbolicProguardRemapResult *result);
void symbolic_sourcemapview_free(SymbolicSourceMapView *source_map);
SymbolicSourceMapView *symbolic_sourcemapview_from_json_slice(const char *data, uintptr_t len);
uint32_t symbolic_sourcemapview_get_source_count(const SymbolicSourceMapView *source_map);
SymbolicStr symbolic_sourcemapview_get_source_name(const SymbolicSourceMapView *source_map, uint32_t index);
const SymbolicSourceView *symbolic_sourcemapview_get_sourceview(const SymbolicSourceMapView *source_map, uint32_t index);
SymbolicTokenMatch *symbolic_sourcemapview_get_token(const SymbolicSourceMapView *source_map, uint32_t index);
uint32_t symbolic_sourcemapview_get_tokens(const SymbolicSourceMapView *source_map);
SymbolicTokenMatch *symbolic_sourcemapview_lookup_token(const SymbolicSourceMapView *source_map, uint32_t line, uint32_t col);
SymbolicTokenMatch *symbolic_sourcemapview_lookup_token_with_function_name(const SymbolicSourceMapView *source_map, uint32_t line, uint32_t col, const SymbolicStr *minified_name, const SymbolicSourceView *view);
SymbolicStr symbolic_sourceview_as_str(const SymbolicSourceView *view);
void symbolic_sourceview_free(SymbolicSourceView *view);
SymbolicSourceView *symbolic_sourceview_from_bytes(const char *bytes, uintptr_t len);
SymbolicStr symbolic_sourceview_get_line(const SymbolicSourceView *view, uint32_t index);
uint32_t symbolic_sourceview_get_line_count(const SymbolicSourceView *source_map);
void symbolic_str_free(SymbolicStr *string);
SymbolicStr symbolic_str_from_cstr(const char *string);
void symbolic_symcache_free(SymbolicSymCache *symcache);
SymbolicSymCache *symbolic_symcache_from_bytes(const uint8_t *bytes, uintptr_t len);
SymbolicSymCache *symbolic_symcache_from_object(const SymbolicObject *object);
SymbolicStr symbolic_symcache_get_arch(const SymbolicSymCache *symcache);
const uint8_t *symbolic_symcache_get_bytes(const SymbolicSymCache *symcache);
SymbolicStr symbolic_symcache_get_debug_id(const SymbolicSymCache *symcache);
uintptr_t symbolic_symcache_get_size(const SymbolicSymCache *symcache);
uint32_t symbolic_symcache_get_version(const SymbolicSymCache *symcache);
int symbolic_symcache_has_file_info(const SymbolicSymCache *symcache);
int symbolic_symcache_has_line_info(const SymbolicSymCache *symcache);
uint32_t symbolic_symcache_latest_version(void);
SymbolicLookupResult *symbolic_symcache_lookup(const SymbolicSymCache *symcache, uint64_t addr);
SymbolicSymCache *symbolic_symcache_open(const char *path);
void symbolic_token_match_free(SymbolicTokenMatch *token_match);
SymbolicUnreal4File *symbolic_unreal4_crash_file_by_index(const SymbolicUnreal4Crash *unreal, uintptr_t index);
uintptr_t symbolic_unreal4_crash_file_count(const SymbolicUnreal4Crash *unreal);
void symbolic_unreal4_crash_free(SymbolicUnreal4Crash *unreal);
SymbolicUnreal4Crash *symbolic_unreal4_crash_from_bytes(const char *bytes, uintptr_t len);
const uint8_t *symbolic_unreal4_file_data(const SymbolicUnreal4File *file, uintptr_t *len);
void symbolic_unreal4_file_free(SymbolicUnreal4File *file);
SymbolicStr symbolic_unreal4_file_name(const SymbolicUnreal4File *file);
SymbolicStr symbolic_unreal4_file_type(const SymbolicUnreal4File *file);
SymbolicStr symbolic_unreal4_get_context(const SymbolicUnreal4Crash *unreal);
SymbolicStr symbolic_unreal4_get_logs(const SymbolicUnreal4Crash *unreal);
int symbolic_uuid_is_nil(const SymbolicUuid *uuid);
SymbolicStr symbolic_uuid_to_str(const SymbolicUuid *uuid);
""")

def load_library():
    module_dir = os.path.dirname(__file__)

    if sys.platform.startswith("linux"):
        lib_name = "_lowlevel__lib.so"
    elif sys.platform == "darwin":
        lib_name = "_lowlevel__lib.dylib"
    else:
        raise ImportError("Unsupported platform: %s" % sys.platform)

    lib_path = os.path.join(module_dir, lib_name)

    if not os.path.exists(lib_path):
        raise ImportError("Could not find library at: %s" % lib_path)

    return ffi.dlopen(lib_path)

lib = load_library()