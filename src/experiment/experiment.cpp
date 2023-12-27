#include "version/git_version.h"

#include <iostream>


int main()
{
    namespace version = gaos::version;

    std::cout
      << std::endl
      << "          * * * * * ** * * * * " << std::endl
      << "         * * * Classgen-1 * * * " << std::endl
      << "          * * * * ** * * * * * " << std::endl
      << std::endl
      << version::get_git_essential_version() << std::endl
      << version::get_compile_stamp() << std::endl
      << std::endl
      << version::get_git_history() << std::endl
      << std::endl;

    return 0;
}